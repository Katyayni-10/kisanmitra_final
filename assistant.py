
import os
import re
from pathlib import Path

from knowledge import EMERGENCY_KEYWORDS, kb_as_text


def _load_env_file() -> None:
    path = Path(__file__).resolve().parent / ".env"
    if not path.is_file():
        return
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-16")
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.lower().startswith("export "):
            line = line[7:]
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and not os.environ.get(key):
            os.environ[key] = value


_load_env_file()

DEFAULT_MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b"]


def candidate_models() -> list:
    env = os.environ.get("KISANMITRA_LLM", "").strip()
    return ([env] if env else []) + [m for m in DEFAULT_MODELS if m != env]
MAX_HISTORY_MESSAGES = 12
LOW_CONF = 0.60

SYSTEM_PROMPT = """You are KisanMitra, a patient and respectful voice helper for farmers, rural families and elderly people in India, \
who may not read well or may be new to technology. Your reply will be READ ALOUD by a text-to-speech voice.

STYLE
- Reply ONLY in <<LANG>>. Use simple everyday words and short sentences, in a warm and respectful tone.
- Keep it short: about 3 to 5 sentences, unless the person asks for full steps or you are explaining a crop result (then up to 6 short sentences).
- Plain text only. No markdown, no asterisks, no bullet symbols, no emojis, no tables. For steps say "First", "Second", "Third" in the reply language.
- If the person seems confused, say it again in simpler words. Never make them feel foolish.

RULES
- Crop problems: use the CROP PHOTO RESULT below. Explain in this order: what the problem is, why it happens, what to do now (low-cost and organic steps first, then chemical options by generic active ingredient name, never brand names), and how to prevent it. Never give exact pesticide quantities; tell them to follow the product label and confirm with the nearest Krishi Vigyan Kendra (KVK) or agriculture officer. The result is a computer guess and can be wrong. If confidence is below 60 percent, say it is uncertain and ask for a clearer photo of one leaf in daylight. If the plant is healthy, say so and give 2 or 3 care tips. If the damage sounds serious, also mention crop insurance (PM Fasal Bima Yojana, report within 72 hours) and the Kisan Credit Card, using KNOWLEDGE.
- Government schemes: use ONLY the facts in KNOWLEDGE below. If the scheme is not there, or you are not sure, say so honestly and send them to the nearest Common Service Centre (CSC), the gram panchayat office, or the official helpline. Never invent amounts, dates or eligibility rules.
- Forms and applications: ask ONE short question at a time (for example "Do you have an Aadhaar card?"), then tell them which documents to carry and what the next step is.
- Health: give general information only. Do not diagnose and do not give medicine doses. Suggest the ASHA worker, the nearest primary health centre or a doctor. For serious symptoms (chest pain, trouble breathing, unconsciousness, heavy bleeding, snake bite, poisoning, stroke signs) the FIRST sentence must tell them to call 108 or 112 immediately.
- Safety: never ask for or accept an OTP, PIN, password, Aadhaar number or bank details. If they describe a suspicious call, link or payment request, warn them not to share anything and to call 1930.
- If asked about something unrelated and harmless, answer briefly. Politely refuse anything harmful.

<<MODE>>

<<CROP>>

KNOWLEDGE (use this for scheme questions):
<<KB>>

FINAL REMINDER: write your entire reply in <<LANG>>, even when the question, the crop name or the disease name is in English. Only unavoidable proper names (such as PM-KISAN) may stay as they are.
"""

MODE_HINTS = {
    "general": "FOCUS: The person may ask about anything. Work out what they need.",
    "crop": "FOCUS: Crop and farming problems. Use the crop photo result if there is one; otherwise ask them to take a clear photo of one leaf using the camera section.",
    "schemes": "FOCUS: Government schemes. Explain who can get it, the benefit, documents and where to apply.",
    "health": "FOCUS: General health information and when to see a doctor. No diagnosis, no dosage.",
    "forms": "FOCUS: Guide them through applying or filling a form, one short question at a time.",
}

NO_KEY_MESSAGE = "KisanMitra needs a Groq API key to answer. Please set GROQ_API_KEY and restart the app."


def get_client():
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        return None
    from groq import Groq
    return Groq(api_key=key)


def crop_context_text(crop: dict | None) -> str:
    if not crop:
        return ("CROP PHOTO RESULT: none yet. If the person asks about a crop disease, "
                "ask them to take a clear photo of one leaf in the camera section.")
    alts = "; ".join(f"{c} - {d} ({p * 100:.0f}%)" for c, d, p in crop.get("alternatives", [])[1:])
    note = " LOW CONFIDENCE." if crop["confidence"] < LOW_CONF else ""
    return (f"CROP PHOTO RESULT (from an image model, may be wrong): crop = {crop['crop']}, "
            f"condition = {crop['condition']}, confidence = {crop['confidence'] * 100:.0f}%.{note}"
            + (f" Other possibilities: {alts}." if alts else ""))


def build_system_prompt(language: str, mode: str = "general", crop: dict | None = None) -> str:
    return (SYSTEM_PROMPT
            .replace("<<LANG>>", language)
            .replace("<<MODE>>", MODE_HINTS.get(mode, MODE_HINTS["general"]))
            .replace("<<CROP>>", crop_context_text(crop))
            .replace("<<KB>>", kb_as_text()))


def build_messages(history: list, question: str, language: str, mode: str = "general",
                   crop: dict | None = None) -> list:
    
    recent = history[-MAX_HISTORY_MESSAGES:]
    msgs = [{"role": "system", "content": build_system_prompt(language, mode, crop)}]
    msgs += [{"role": m["role"], "content": m["content"]} for m in recent]
    # Repeat the language next to the question itself: models follow the language of the latest message
    msgs.append({"role": "user", "content": f"{question}\n\n(Reply in {language}.)"})
    return msgs


def ask(history: list, question: str, language: str = "Hindi", mode: str = "general",
        crop: dict | None = None) -> str:
    if get_client() is None:
        return NO_KEY_MESSAGE
    text, err = _complete(build_messages(history, question, language, mode, crop), 1500)
    if text:
        return text
    return f"Sorry, I could not answer right now ({type(err).__name__}). Please try again."


def translate_label(crop: str, condition: str, language: str):
    if language.strip().lower() == "english":
        return None
    prompt = (f"Translate this crop name and plant disease name into {language}, using the words farmers use. "
              f"Reply with ONLY the translation in the form: crop - disease. No explanation.\n\n"
              f"Crop: {crop}\nDisease: {condition}")
    text, _ = _complete([{"role": "user", "content": prompt}], 400)
    return text.splitlines()[0].strip() if text else None


def _complete(messages: list, max_tokens: int = 1500):
    client = get_client()
    if client is None:
        return None, None
    last_err = None
    for model in candidate_models():
        kwargs = {}
        if "gpt-oss" in model:
            kwargs["reasoning_effort"] = "low"
        try:
            resp = client.chat.completions.create(
                model=model, messages=messages, max_tokens=max_tokens, temperature=0.3, **kwargs)
            text = (resp.choices[0].message.content or "")
            text = re.sub(r"<think>.*?(</think>|$)", "", text, flags=re.S).strip()
            if text:
                return text, None
            last_err = RuntimeError("empty reply")
        except Exception as e:
            last_err = e
            print(f"[KisanMitra] LLM error with {model}: {e}", flush=True)
            if getattr(e, "status_code", None) in (400, 404):
                continue
            break
    return None, last_err


def is_emergency(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in EMERGENCY_KEYWORDS)


def strip_for_speech(text: str) -> str:
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[*_#`>~|]", "", text)
    text = re.sub(r"^\s*[-•]\s+", "", text, flags=re.M)
    text = re.sub(r"\s*\n+\s*", ". ", text)
    text = re.sub(r"\.\s*\.", ".", text)
    return re.sub(r"\s{2,}", " ", text).strip()