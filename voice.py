"""Speech in (Groq Whisper) and speech out (gTTS)."""
import io
import os

from assistant import get_client

LANGS = {
    "English": "en",
    "Hindi (हिन्दी)": "hi",
    "Punjabi (ਪੰਜਾਬੀ)": "pa",
    "Marathi (मराठी)": "mr",
    "Gujarati (ગુજરાતી)": "gu",
    "Bengali (বাংলা)": "bn",
    "Tamil (தமிழ்)": "ta",
    "Telugu (తెలుగు)": "te",
    "Kannada (ಕನ್ನಡ)": "kn",
    "Malayalam (മലയാളം)": "ml",
}

STT_MODEL = os.environ.get("KISANMITRA_STT", "whisper-large-v3")


def transcribe(audio_bytes: bytes, lang_code: str) -> str:
    client = get_client()
    if client is None:
        return ""
    try:
        result = client.audio.transcriptions.create(
            file=("question.wav", audio_bytes),
            model=STT_MODEL,
            language=lang_code,
        )
        return result.text.strip()
    except Exception:
        return ""


def speak(text: str, lang_code: str) -> bytes:
    from gtts import gTTS
    buf = io.BytesIO()
    gTTS(text=text, lang=lang_code).write_to_fp(buf)
    return buf.getvalue()
