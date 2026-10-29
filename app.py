"""KisanMitra - voice assistant for farmers and rural/elderly users."""
import hashlib
import io
import os
import streamlit as st
from PIL import Image
import assistant
import vision
import voice
from knowledge import EMERGENCY_BANNER, HELPLINES, SCHEMES

import crop_journal
import weather_alerts

st.set_page_config(page_title="KisanMitra", page_icon="🌿", layout="centered")

st.markdown("""
<style>
html, body, [class*="css"] { font-size: 20px; }
.stButton > button { font-size: 1.15rem; min-height: 3.2rem; border-radius: 14px; width: 100%; }
[data-testid="stChatMessage"] p { font-size: 1.25rem; line-height: 1.65; }
h1 { font-size: 2.4rem !important; }
</style>
""", unsafe_allow_html=True)

MODES = {
    "💬 Ask anything": "general",
    "🌿 My crop problem": "crop",
    "🏛️ Government schemes": "schemes",
    "🩺 Health information": "health",
    "📝 Help with a form": "forms",
}

EXAMPLES = {
    "hi": ["किसान सम्मान निधि कैसे मिलेगी?", "फसल खराब हो जाए तो बीमा कैसे मिलेगा?",
           "आयुष्मान कार्ड कैसे बनवाएं?", "फोन पर कोई OTP मांग रहा है, क्या करूं?"],
    "default": ["How do I get PM-KISAN money?", "How do I get crop insurance if my crop is damaged?",
                "How do I make an Ayushman card?", "Someone is asking for my OTP on phone"],
}

PHOTO_QUESTION = ("I uploaded a photo of my crop leaf. Please explain what is wrong, what I should do now, "
                  "and how to prevent it.")

ss = st.session_state
ss.setdefault("history", [])
ss.setdefault("crop", None)
ss.setdefault("last_voice", None)
ss.setdefault("last_img", None)
ss.setdefault("last_photo_bytes", None)
ss.setdefault("fresh_audio", None)
ss.setdefault("last_audio", None)
ss.setdefault("explained_lang", None)
ss.setdefault("label_tr", {})


with st.sidebar:
    st.header("📞 Helplines")
    for name, number in HELPLINES:
        st.write(f"**{number}** - {name}")
    st.caption("Numbers can differ by state. 112 works all over India.")
    with st.expander("🏛️ Schemes KisanMitra knows"):
        for s in SCHEMES:
            st.write("• " + s["name"])
    if st.button("🗑️ Start over"):
        for k in ("history", "crop", "fresh_audio", "last_audio","last_img", "last_photo_bytes", "explained_lang",):
            ss[k] = [] if k == "history" else None
        st.rerun()

st.title("🌿 KisanMitra")
st.caption("Speak in your own language, or show a sick leaf. KisanMitra answers by voice.")

if not os.environ.get("GROQ_API_KEY"):
    st.warning("GROQ_API_KEY is not set, so KisanMitra cannot answer yet. See README.")

lang_name = st.selectbox("Language / भाषा", list(voice.LANGS.keys()), index=1)
lang_code = voice.LANGS[lang_name]
english_lang = lang_name.split(" (")[0]

mode_label = st.radio("What do you need help with?", list(MODES.keys()), horizontal=True)
mode = MODES[mode_label]

question = None
display = None
photo_bytes = None
ask_mode = mode

with st.expander("📷 Check a crop leaf (take or upload a photo)"):
    if not vision.model_available():
        st.info("Crop model not found yet. Train it first with "
                "`python train.py --data <PlantVillage folder>` and keep the `model/` folder next to app.py. "
                "The voice assistant below works without it.")
    else:
        tab_cam, tab_up = st.tabs(["📷 Camera", "🖼️ Upload"])
        with tab_cam:
            cam = st.camera_input("Take a clear photo of ONE leaf in daylight")
        with tab_up:
            up = st.file_uploader("Upload leaf photo", type=["jpg", "jpeg", "png"])
        file = cam or up
        if file is not None:
            data = file.getvalue()
            digest = hashlib.md5(data).hexdigest()
            if digest != ss.last_img:
                ss.last_img = digest
                ss.last_photo_bytes = data
                photo_bytes = data

if photo_bytes is not None:
    try:
        with st.spinner("Looking at the leaf..."):
            ss.crop = vision.predict(Image.open(io.BytesIO(photo_bytes)))
        c = ss.crop
        question = PHOTO_QUESTION
        display = f"📷 {c['crop']} - {c['condition']} ({c['confidence'] * 100:.0f}%)"
        ask_mode = "crop"
        ss.explained_lang = lang_code
    except Exception as e:
        st.error(f"Could not analyse the photo ({type(e).__name__}). Please try another photo.")
        photo_bytes = None

audio = st.audio_input("🎤 Tap the mic, speak, then tap stop")
if audio is not None:
    data = audio.getvalue()
    digest = hashlib.md5(data).hexdigest()
    if digest != ss.last_voice:
        ss.last_voice = digest
        with st.spinner("Listening..."):
            heard = voice.transcribe(data, lang_code)
        if heard:
            if question is None:
                question = heard
        else:
            st.warning("I could not hear that clearly. Please try again, a little closer to the phone.")

st.write("Or tap a question:")
examples = EXAMPLES.get(lang_code, EXAMPLES["default"])
cols = st.columns(2)
for i, ex in enumerate(examples):
    if cols[i % 2].button(ex, key=f"ex{i}") and question is None:
        question = ex

typed = st.chat_input("Or type your question here")
if typed and question is None:
    question = typed

if question is None and ss.crop and ss.explained_lang and ss.explained_lang != lang_code:
    question = PHOTO_QUESTION
    display = f"🌐 Explain again in {english_lang}"
    ask_mode = "crop"
    ss.explained_lang = lang_code

if question:
    emergency = assistant.is_emergency(question)
    with st.spinner("Thinking..."):
        reply = assistant.ask(ss.history, question, english_lang, ask_mode, ss.crop)
    ss.history += [
        {"role": "user", "content": question, "display": display,
         "image": photo_bytes},
        {"role": "assistant", "content": reply, "emergency": emergency},
    ]
    try:
        ss.fresh_audio = voice.speak(assistant.strip_for_speech(reply), lang_code)
    except Exception:
        ss.fresh_audio = None
        st.caption("🔇 Voice reply needs internet. Showing text only.")

if ss.crop:
    c = ss.crop
    tr = None
    if english_lang != "English":
        tr_key = (c["label"], english_lang)
        if tr_key not in ss.label_tr:
            ss.label_tr[tr_key] = assistant.translate_label(c["crop"], c["condition"], english_lang)
        tr = ss.label_tr[tr_key]
    if tr:
        st.subheader(f"🌿 {tr}")
        st.caption(f"{c['crop']} - {c['condition']}")
    else:
        st.subheader(f"🌿 {c['crop']} - {c['condition']}")
    st.progress(min(c["confidence"], 1.0), text=f"Confidence: {c['confidence'] * 100:.0f}%")
    if c["confidence"] < assistant.LOW_CONF:
        st.warning("Not sure about this one. Try a clearer, closer photo of a single leaf.")
    with st.expander("Other possibilities"):
        for crop_name, cond, p in c["alternatives"]:
            st.write(f"{crop_name} - {cond}: {p * 100:.1f}%")

st.divider()
crop_journal.render_journal(
    crop=ss.crop,
    photo_bytes=ss.last_photo_bytes,
    lang_code=lang_code,
)
st.divider()

st.divider()
weather_alerts.render_weather_alerts(lang_name)
st.divider()

for m in ss.history:
    with st.chat_message(m["role"]):
        if m.get("image"):
            st.image(m["image"], width=220)
        st.write(m.get("display") or m["content"])
        if m.get("emergency"):
            st.error(EMERGENCY_BANNER)

if ss.fresh_audio:
    ss.last_audio = ss.fresh_audio
    st.audio(ss.fresh_audio, format="audio/mp3", autoplay=True)
    ss.fresh_audio = None
elif ss.last_audio:
    st.audio(ss.last_audio, format="audio/mp3")

st.divider()
st.caption("⚠️ KisanMitra gives general information only, not medical, legal or professional advice. "
           "Confirm crop treatments with your Krishi Vigyan Kendra (KVK) and scheme details at your nearest "
           "Common Service Centre (CSC) or gram panchayat.")