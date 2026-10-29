
"""Crop Health Journal for KisanMitra."""
import json
import uuid
from datetime import datetime
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "crop_journal_data"
IMAGE_DIR = DATA_DIR / "images"
JOURNAL_FILE = DATA_DIR / "journal.json"


TEXT = {
    "en": {
        "title": "📔 Crop Health Journal",
        "intro": "Save plant diagnoses, record follow-up observations, and review changes over time.",
        "save": "➕ Save current diagnosis",
        "crop": "Crop",
        "condition": "Predicted condition",
        "confidence": "Model confidence",
        "confidence_note": "Confidence is the model's score, not a guarantee of correctness.",
        "symptoms": "Symptoms you noticed (optional)",
        "symptoms_hint": "e.g. brown spots near the leaf edges",
        "save_button": "Save to Crop Health Journal",
        "saved": "Diagnosis saved to your journal!",
        "save_error": "Could not save the entry. Check folder permissions.",
        "history": "Your plant history",
        "empty": "Your journal is empty. Analyze a leaf, then save the diagnosis here.",
        "entries": "saved diagnosis(es)",
        "recorded": "Recorded",
        "photo": "Saved leaf photo",
        "initial": "Initial symptoms",
        "alternatives": "Other model predictions at the time",
        "timeline": "Follow-up timeline",
        "no_observations": "No follow-up observations yet.",
        "current": "How does the plant look now?",
        "unchanged": "No visible change",
        "improved": "Symptoms appear improved",
        "worse": "Symptoms appear worse",
        "new": "New symptoms noticed",
        "notes": "Observation notes (optional)",
        "notes_hint": "Describe what you see today...",
        "add": "Add observation",
        "added": "Observation added!",
        "missing": "This journal entry could not be found.",
        "read_error": "The journal file could not be read. Check its contents.",
        "observation_error": "Could not save the observation.",
        "original": "Original model confidence",
    },
    "hi": {
        "title": "📔 फसल स्वास्थ्य डायरी",
        "intro": "फसल की जाँच सेव करें और समय के साथ बदलाव दर्ज करें।",
        "save": "➕ वर्तमान जाँच सेव करें",
        "crop": "फसल",
        "condition": "अनुमानित बीमारी",
        "confidence": "मॉडल का विश्वास स्तर",
        "confidence_note": "यह मॉडल का अनुमान है, सही होने की गारंटी नहीं।",
        "symptoms": "दिखने वाले लक्षण (वैकल्पिक)",
        "symptoms_hint": "जैसे पत्तियों के किनारों पर भूरे धब्बे",
        "save_button": "फसल डायरी में सेव करें",
        "saved": "जाँच डायरी में सेव हो गई!",
        "save_error": "रिकॉर्ड सेव नहीं हुआ। फ़ोल्डर की अनुमति जाँचें।",
        "history": "आपकी फसल का इतिहास",
        "empty": "डायरी खाली है। पत्ती की जाँच करके रिकॉर्ड सेव करें।",
        "entries": "जाँच रिकॉर्ड",
        "recorded": "दर्ज किया गया",
        "photo": "सेव की गई पत्ती की तस्वीर",
        "initial": "शुरुआती लक्षण",
        "alternatives": "मॉडल के अन्य अनुमान",
        "timeline": "आगे की स्थिति",
        "no_observations": "अभी कोई नई जानकारी दर्ज नहीं है।",
        "current": "अब पौधा कैसा दिख रहा है?",
        "unchanged": "कोई स्पष्ट बदलाव नहीं",
        "improved": "लक्षणों में सुधार दिख रहा है",
        "worse": "लक्षण बढ़ते दिख रहे हैं",
        "new": "नए लक्षण दिखाई दिए",
        "notes": "आज की जानकारी (वैकल्पिक)",
        "notes_hint": "आज आपको क्या दिखाई दे रहा है?",
        "add": "जानकारी जोड़ें",
        "added": "जानकारी जोड़ दी गई!",
        "missing": "यह रिकॉर्ड नहीं मिला।",
        "read_error": "डायरी फ़ाइल पढ़ी नहीं जा सकी।",
        "observation_error": "जानकारी सेव नहीं हो सकी।",
        "original": "मूल मॉडल विश्वास स्तर",
    },
    "pa": {
        "title": "📔 ਫ਼ਸਲ ਸਿਹਤ ਡਾਇਰੀ",
        "intro": "ਫ਼ਸਲ ਦੀ ਜਾਂਚ ਸੇਵ ਕਰੋ ਅਤੇ ਸਮੇਂ ਨਾਲ ਬਦਲਾਅ ਦਰਜ ਕਰੋ।",
        "save": "➕ ਮੌਜੂਦਾ ਜਾਂਚ ਸੇਵ ਕਰੋ",
        "crop": "ਫ਼ਸਲ",
        "condition": "ਅਨੁਮਾਨਿਤ ਬਿਮਾਰੀ",
        "confidence": "ਮਾਡਲ ਦਾ ਭਰੋਸਾ ਪੱਧਰ",
        "confidence_note": "ਇਹ ਮਾਡਲ ਦਾ ਅਨੁਮਾਨ ਹੈ, ਸਹੀ ਹੋਣ ਦੀ ਗਾਰੰਟੀ ਨਹੀਂ।",
        "symptoms": "ਦਿਖਾਈ ਦੇਣ ਵਾਲੇ ਲੱਛਣ (ਵਿਕਲਪਿਕ)",
        "symptoms_hint": "ਜਿਵੇਂ ਪੱਤਿਆਂ ਦੇ ਕਿਨਾਰਿਆਂ 'ਤੇ ਭੂਰੇ ਧੱਬੇ",
        "save_button": "ਫ਼ਸਲ ਡਾਇਰੀ ਵਿੱਚ ਸੇਵ ਕਰੋ",
        "saved": "ਜਾਂਚ ਡਾਇਰੀ ਵਿੱਚ ਸੇਵ ਹੋ ਗਈ!",
        "save_error": "ਰਿਕਾਰਡ ਸੇਵ ਨਹੀਂ ਹੋਇਆ। ਫੋਲਡਰ ਦੀ ਇਜਾਜ਼ਤ ਜਾਂਚੋ।",
        "history": "ਤੁਹਾਡੀ ਫ਼ਸਲ ਦਾ ਇਤਿਹਾਸ",
        "empty": "ਡਾਇਰੀ ਖਾਲੀ ਹੈ। ਪੱਤੇ ਦੀ ਜਾਂਚ ਕਰਕੇ ਰਿਕਾਰਡ ਸੇਵ ਕਰੋ।",
        "entries": "ਜਾਂਚ ਰਿਕਾਰਡ",
        "recorded": "ਦਰਜ ਕੀਤਾ",
        "photo": "ਸੇਵ ਕੀਤੀ ਪੱਤੇ ਦੀ ਤਸਵੀਰ",
        "initial": "ਸ਼ੁਰੂਆਤੀ ਲੱਛਣ",
        "alternatives": "ਮਾਡਲ ਦੇ ਹੋਰ ਅਨੁਮਾਨ",
        "timeline": "ਅਗਲੀ ਸਥਿਤੀ",
        "no_observations": "ਹਾਲੇ ਕੋਈ ਨਵੀਂ ਜਾਣਕਾਰੀ ਦਰਜ ਨਹੀਂ ਹੈ।",
        "current": "ਹੁਣ ਪੌਦਾ ਕਿਹੋ ਜਿਹਾ ਦਿਖਦਾ ਹੈ?",
        "unchanged": "ਕੋਈ ਸਪੱਸ਼ਟ ਬਦਲਾਅ ਨਹੀਂ",
        "improved": "ਲੱਛਣਾਂ ਵਿੱਚ ਸੁਧਾਰ ਦਿਖਦਾ ਹੈ",
        "worse": "ਲੱਛਣ ਵਧਦੇ ਦਿਖਦੇ ਹਨ",
        "new": "ਨਵੇਂ ਲੱਛਣ ਦਿਖੇ",
        "notes": "ਅੱਜ ਦੀ ਜਾਣਕਾਰੀ (ਵਿਕਲਪਿਕ)",
        "notes_hint": "ਅੱਜ ਤੁਹਾਨੂੰ ਕੀ ਦਿਖਾਈ ਦੇ ਰਿਹਾ ਹੈ?",
        "add": "ਜਾਣਕਾਰੀ ਸ਼ਾਮਲ ਕਰੋ",
        "added": "ਜਾਣਕਾਰੀ ਸ਼ਾਮਲ ਹੋ ਗਈ!",
        "missing": "ਇਹ ਰਿਕਾਰਡ ਨਹੀਂ ਮਿਲਿਆ।",
        "read_error": "ਡਾਇਰੀ ਫ਼ਾਈਲ ਪੜ੍ਹੀ ਨਹੀਂ ਜਾ ਸਕੀ।",
        "observation_error": "ਜਾਣਕਾਰੀ ਸੇਵ ਨਹੀਂ ਹੋ ਸਕੀ।",
        "original": "ਮੂਲ ਮਾਡਲ ਭਰੋਸਾ ਪੱਧਰ",
    },
    "mr": {
        "title": "📔 पीक आरोग्य दिनदर्शिका",
        "intro": "पिकाची तपासणी जतन करा आणि कालांतराने होणारे बदल नोंदवा.",
        "save": "➕ सध्याची तपासणी जतन करा",
        "crop": "पीक",
        "condition": "अंदाजित रोग",
        "confidence": "मॉडेलचा विश्वास स्तर",
        "confidence_note": "हा मॉडेलचा अंदाज आहे; अचूकतेची हमी नाही.",
        "symptoms": "दिसलेली लक्षणे (ऐच्छिक)",
        "symptoms_hint": "उदा. पानांच्या कडांवर तपकिरी डाग",
        "save_button": "पीक दिनदर्शिकेत जतन करा",
        "saved": "तपासणी जतन झाली!",
        "save_error": "नोंद जतन झाली नाही. फोल्डरची परवानगी तपासा.",
        "history": "तुमच्या पिकाचा इतिहास",
        "empty": "दिनदर्शिका रिकामी आहे. पान तपासून नोंद जतन करा.",
        "entries": "तपासणी नोंदी",
        "recorded": "नोंदवले",
        "photo": "जतन केलेला पानाचा फोटो",
        "initial": "सुरुवातीची लक्षणे",
        "alternatives": "मॉडेलचे इतर अंदाज",
        "timeline": "पुढील निरीक्षणे",
        "no_observations": "अद्याप निरीक्षणे नोंदवलेली नाहीत.",
        "current": "आता रोप कसे दिसते?",
        "unchanged": "विशेष बदल नाही",
        "improved": "लक्षणे सुधारत असल्याचे दिसते",
        "worse": "लक्षणे वाढत असल्याचे दिसते",
        "new": "नवीन लक्षणे दिसली",
        "notes": "आजची निरीक्षणे (ऐच्छिक)",
        "notes_hint": "आज काय दिसले ते लिहा...",
        "add": "निरीक्षण जोडा",
        "added": "निरीक्षण जोडले!",
        "missing": "ही नोंद सापडली नाही.",
        "read_error": "दिनदर्शिका फाइल वाचता आली नाही.",
        "observation_error": "निरीक्षण जतन करता आले नाही.",
        "original": "मूळ मॉडेल विश्वास स्तर",
    },
    "gu": {
        "title": "📔 પાક આરોગ્ય ડાયરી",
        "intro": "પાકનું નિદાન સાચવો અને સમય સાથે થતા ફેરફારો નોંધો.",
        "save": "➕ હાલનું નિદાન સાચવો",
        "crop": "પાક",
        "condition": "અનુમાનિત રોગ",
        "confidence": "મોડેલનો વિશ્વાસ સ્તર",
        "confidence_note": "આ મોડેલનો અંદાજ છે, ચોકસાઈની ખાતરી નથી.",
        "symptoms": "દેખાતા લક્ષણો (વૈકલ્પિક)",
        "symptoms_hint": "દા.ત. પાંદડાની કિનારીઓ પર ભૂરા ડાઘ",
        "save_button": "પાક ડાયરીમાં સાચવો",
        "saved": "નિદાન ડાયરીમાં સાચવાયું!",
        "save_error": "નોંધ સાચવી શકાઈ નહીં. ફોલ્ડરની પરવાનગી તપાસો.",
        "history": "તમારા પાકનો ઇતિહાસ",
        "empty": "ડાયરી ખાલી છે. પાનનું નિદાન કરીને નોંધ સાચવો.",
        "entries": "નિદાન નોંધો",
        "recorded": "નોંધાયેલ",
        "photo": "સાચવેલો પાનનો ફોટો",
        "initial": "શરૂઆતનાં લક્ષણો",
        "alternatives": "મોડેલનાં અન્ય અનુમાનો",
        "timeline": "આગળનાં નિરીક્ષણો",
        "no_observations": "હજુ કોઈ નિરીક્ષણ નોંધાયું નથી.",
        "current": "હવે છોડ કેવો દેખાય છે?",
        "unchanged": "કોઈ દેખીતો ફેરફાર નથી",
        "improved": "લક્ષણોમાં સુધારો દેખાય છે",
        "worse": "લક્ષણો વધતાં દેખાય છે",
        "new": "નવા લક્ષણો દેખાયા",
        "notes": "આજનું નિરીક્ષણ (વૈકલ્પિક)",
        "notes_hint": "આજે શું દેખાય છે તે લખો...",
        "add": "નિરીક્ષણ ઉમેરો",
        "added": "નિરીક્ષણ ઉમેરાયું!",
        "missing": "આ નોંધ મળી નથી.",
        "read_error": "ડાયરી ફાઇલ વાંચી શકાઈ નથી.",
        "observation_error": "નિરીક્ષણ સાચવી શકાયું નથી.",
        "original": "મૂળ મોડેલ વિશ્વાસ સ્તર",
    },
    "bn": {
        "title": "📔 ফসলের স্বাস্থ্য ডায়েরি",
        "intro": "ফসলের রোগ নির্ণয় সংরক্ষণ করুন এবং সময়ের সঙ্গে পরিবর্তন লিখুন।",
        "save": "➕ বর্তমান রোগ নির্ণয় সংরক্ষণ করুন",
        "crop": "ফসল",
        "condition": "সম্ভাব্য রোগ",
        "confidence": "মডেলের আস্থার মাত্রা",
        "confidence_note": "এটি মডেলের অনুমান, সঠিক হওয়ার নিশ্চয়তা নয়।",
        "symptoms": "দেখা লক্ষণ (ঐচ্ছিক)",
        "symptoms_hint": "যেমন পাতার কিনারায় বাদামি দাগ",
        "save_button": "ফসলের ডায়েরিতে সংরক্ষণ করুন",
        "saved": "রোগ নির্ণয় ডায়েরিতে সংরক্ষিত হয়েছে!",
        "save_error": "তথ্য সংরক্ষণ করা যায়নি। ফোল্ডারের অনুমতি পরীক্ষা করুন।",
        "history": "আপনার ফসলের ইতিহাস",
        "empty": "ডায়েরি খালি। পাতার ছবি পরীক্ষা করে তথ্য সংরক্ষণ করুন।",
        "entries": "টি সংরক্ষিত রেকর্ড",
        "recorded": "নথিভুক্ত",
        "photo": "সংরক্ষিত পাতার ছবি",
        "initial": "প্রাথমিক লক্ষণ",
        "alternatives": "মডেলের অন্যান্য অনুমান",
        "timeline": "পরবর্তী পর্যবেক্ষণ",
        "no_observations": "এখনও কোনো পর্যবেক্ষণ নেই।",
        "current": "এখন গাছটি কেমন দেখাচ্ছে?",
        "unchanged": "চোখে পড়ার মতো পরিবর্তন নেই",
        "improved": "লক্ষণ কিছুটা ভালো মনে হচ্ছে",
        "worse": "লক্ষণ বাড়ছে বলে মনে হচ্ছে",
        "new": "নতুন লক্ষণ দেখা গেছে",
        "notes": "আজকের পর্যবেক্ষণ (ঐচ্ছিক)",
        "notes_hint": "আজ কী দেখছেন লিখুন...",
        "add": "পর্যবেক্ষণ যোগ করুন",
        "added": "পর্যবেক্ষণ যোগ করা হয়েছে!",
        "missing": "এই রেকর্ডটি পাওয়া যায়নি।",
        "read_error": "ডায়েরির ফাইল পড়া যায়নি।",
        "observation_error": "পর্যবেক্ষণ সংরক্ষণ করা যায়নি।",
        "original": "মূল মডেলের আস্থার মাত্রা",
    },
    "ta": {
        "title": "📔 பயிர் நலக் குறிப்பேடு",
        "intro": "பயிர் கண்டறிதலைச் சேமித்து, காலப்போக்கில் ஏற்படும் மாற்றங்களைப் பதிவு செய்யுங்கள்.",
        "save": "➕ தற்போதைய கண்டறிதலைச் சேமிக்கவும்",
        "crop": "பயிர்",
        "condition": "கணிக்கப்பட்ட நோய்",
        "confidence": "மாதிரியின் நம்பிக்கை அளவு",
        "confidence_note": "இது மாதிரியின் மதிப்பீடு; சரியானது என்பதற்கான உத்தரவாதம் அல்ல.",
        "symptoms": "நீங்கள் கவனித்த அறிகுறிகள் (விருப்பம்)",
        "symptoms_hint": "எ.கா. இலை ஓரங்களில் பழுப்பு நிறப் புள்ளிகள்",
        "save_button": "பயிர் குறிப்பேட்டில் சேமிக்கவும்",
        "saved": "கண்டறிதல் சேமிக்கப்பட்டது!",
        "save_error": "பதிவைச் சேமிக்க முடியவில்லை. கோப்புறை அனுமதியைச் சரிபார்க்கவும்.",
        "history": "உங்கள் பயிரின் வரலாறு",
        "empty": "குறிப்பேடு காலியாக உள்ளது. இலையைப் பரிசோதித்து பதிவைச் சேமிக்கவும்.",
        "entries": "சேமித்த பதிவுகள்",
        "recorded": "பதிவு செய்யப்பட்ட நாள்",
        "photo": "சேமித்த இலைப் படம்",
        "initial": "ஆரம்ப அறிகுறிகள்",
        "alternatives": "மாதிரியின் பிற கணிப்புகள்",
        "timeline": "தொடர் கண்காணிப்பு",
        "no_observations": "தொடர் கண்காணிப்புகள் எதுவும் இல்லை.",
        "current": "இப்போது செடி எப்படி உள்ளது?",
        "unchanged": "குறிப்பிடத்தக்க மாற்றமில்லை",
        "improved": "அறிகுறிகள் மேம்பட்டுள்ளன",
        "worse": "அறிகுறிகள் அதிகரித்துள்ளன",
        "new": "புதிய அறிகுறிகள் காணப்பட்டன",
        "notes": "இன்றைய குறிப்புகள் (விருப்பம்)",
        "notes_hint": "இன்று நீங்கள் கவனித்ததை எழுதுங்கள்...",
        "add": "குறிப்பைச் சேர்க்கவும்",
        "added": "குறிப்பு சேர்க்கப்பட்டது!",
        "missing": "இந்தப் பதிவு கிடைக்கவில்லை.",
        "read_error": "குறிப்பேட்டுக் கோப்பைப் படிக்க முடியவில்லை.",
        "observation_error": "குறிப்பைச் சேமிக்க முடியவில்லை.",
        "original": "முதன்மை மாதிரியின் நம்பிக்கை அளவு",
    },
    "te": {
        "title": "📔 పంట ఆరోగ్య డైరీ",
        "intro": "పంట నిర్ధారణను భద్రపరచి, కాలక్రమంలో మార్పులను నమోదు చేయండి.",
        "save": "➕ ప్రస్తుత నిర్ధారణను భద్రపరచండి",
        "crop": "పంట",
        "condition": "అంచనా వేసిన వ్యాధి",
        "confidence": "మోడల్ విశ్వాస స్థాయి",
        "confidence_note": "ఇది మోడల్ అంచనా మాత్రమే; ఖచ్చితత్వానికి హామీ కాదు.",
        "symptoms": "మీరు గమనించిన లక్షణాలు (ఐచ్ఛికం)",
        "symptoms_hint": "ఉదా. ఆకుల అంచుల వద్ద గోధుమ రంగు మచ్చలు",
        "save_button": "పంట డైరీలో భద్రపరచండి",
        "saved": "నిర్ధారణ డైరీలో భద్రపరచబడింది!",
        "save_error": "రికార్డును భద్రపరచలేకపోయాం. ఫోల్డర్ అనుమతులను తనిఖీ చేయండి.",
        "history": "మీ పంట చరిత్ర",
        "empty": "డైరీ ఖాళీగా ఉంది. ఆకు పరీక్షించి రికార్డును భద్రపరచండి.",
        "entries": "భద్రపరిచిన రికార్డులు",
        "recorded": "నమోదైన తేదీ",
        "photo": "భద్రపరిచిన ఆకు ఫోటో",
        "initial": "ప్రారంభ లక్షణాలు",
        "alternatives": "మోడల్ ఇతర అంచనాలు",
        "timeline": "తదుపరి పరిశీలనలు",
        "no_observations": "ఇంకా పరిశీలనలు నమోదు కాలేదు.",
        "current": "ఇప్పుడు మొక్క ఎలా కనిపిస్తోంది?",
        "unchanged": "గమనించదగిన మార్పు లేదు",
        "improved": "లక్షణాలు మెరుగుపడినట్లు ఉన్నాయి",
        "worse": "లక్షణాలు పెరిగినట్లు ఉన్నాయి",
        "new": "కొత్త లక్షణాలు కనిపించాయి",
        "notes": "ఈరోజు పరిశీలనలు (ఐచ్ఛికం)",
        "notes_hint": "ఈరోజు మీరు గమనించినది రాయండి...",
        "add": "పరిశీలనను జోడించండి",
        "added": "పరిశీలన జోడించబడింది!",
        "missing": "ఈ రికార్డు కనబడలేదు.",
        "read_error": "డైరీ ఫైల్ చదవలేకపోయాం.",
        "observation_error": "పరిశీలనను భద్రపరచలేకపోయాం.",
        "original": "అసలు మోడల్ విశ్వాస స్థాయి",
    },
    "kn": {
        "title": "📔 ಬೆಳೆ ಆರೋಗ್ಯ ದಿನಚರಿ",
        "intro": "ಬೆಳೆ ರೋಗನಿರ್ಣಯವನ್ನು ಉಳಿಸಿ ಮತ್ತು ಕಾಲಕ್ರಮದಲ್ಲಿ ಆಗುವ ಬದಲಾವಣೆಗಳನ್ನು ದಾಖಲಿಸಿ.",
        "save": "➕ ಪ್ರಸ್ತುತ ರೋಗನಿರ್ಣಯವನ್ನು ಉಳಿಸಿ",
        "crop": "ಬೆಳೆ",
        "condition": "ಊಹಿಸಲಾದ ರೋಗ",
        "confidence": "ಮಾದರಿಯ ವಿಶ್ವಾಸ ಮಟ್ಟ",
        "confidence_note": "ಇದು ಮಾದರಿಯ ಅಂದಾಜು ಮಾತ್ರ; ನಿಖರತೆಯ ಖಾತರಿ ಅಲ್ಲ.",
        "symptoms": "ನೀವು ಗಮನಿಸಿದ ಲಕ್ಷಣಗಳು (ಐಚ್ಛಿಕ)",
        "symptoms_hint": "ಉದಾ. ಎಲೆಯ ಅಂಚಿನಲ್ಲಿ ಕಂದು ಕಲೆಗಳು",
        "save_button": "ಬೆಳೆ ದಿನಚರಿಯಲ್ಲಿ ಉಳಿಸಿ",
        "saved": "ರೋಗನಿರ್ಣಯ ಉಳಿಸಲಾಗಿದೆ!",
        "save_error": "ದಾಖಲೆಯನ್ನು ಉಳಿಸಲಾಗಲಿಲ್ಲ. ಫೋಲ್ಡರ್ ಅನುಮತಿಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "history": "ನಿಮ್ಮ ಬೆಳೆಯ ಇತಿಹಾಸ",
        "empty": "ದಿನಚರಿ ಖಾಲಿಯಾಗಿದೆ. ಎಲೆಯನ್ನು ಪರೀಕ್ಷಿಸಿ ದಾಖಲೆಯನ್ನು ಉಳಿಸಿ.",
        "entries": "ಉಳಿಸಿದ ದಾಖಲೆಗಳು",
        "recorded": "ದಾಖಲಿಸಿದ ದಿನಾಂಕ",
        "photo": "ಉಳಿಸಿದ ಎಲೆಯ ಚಿತ್ರ",
        "initial": "ಆರಂಭಿಕ ಲಕ್ಷಣಗಳು",
        "alternatives": "ಮಾದರಿಯ ಇತರ ಊಹೆಗಳು",
        "timeline": "ಮುಂದಿನ ವೀಕ್ಷಣೆಗಳು",
        "no_observations": "ಇನ್ನೂ ಯಾವುದೇ ವೀಕ್ಷಣೆಗಳನ್ನು ದಾಖಲಿಸಿಲ್ಲ.",
        "current": "ಈಗ ಸಸ್ಯ ಹೇಗೆ ಕಾಣುತ್ತದೆ?",
        "unchanged": "ಗಮನಾರ್ಹ ಬದಲಾವಣೆ ಇಲ್ಲ",
        "improved": "ಲಕ್ಷಣಗಳು ಸುಧಾರಿಸಿದಂತೆ ಕಾಣುತ್ತವೆ",
        "worse": "ಲಕ್ಷಣಗಳು ಹೆಚ್ಚಾದಂತೆ ಕಾಣುತ್ತವೆ",
        "new": "ಹೊಸ ಲಕ್ಷಣಗಳು ಕಂಡುಬಂದಿವೆ",
        "notes": "ಇಂದಿನ ವೀಕ್ಷಣೆಗಳು (ಐಚ್ಛಿಕ)",
        "notes_hint": "ಇಂದು ನೀವು ಗಮನಿಸಿದ್ದನ್ನು ಬರೆಯಿರಿ...",
        "add": "ವೀಕ್ಷಣೆ ಸೇರಿಸಿ",
        "added": "ವೀಕ್ಷಣೆ ಸೇರಿಸಲಾಗಿದೆ!",
        "missing": "ಈ ದಾಖಲೆ ಕಂಡುಬಂದಿಲ್ಲ.",
        "read_error": "ದಿನಚರಿ ಫೈಲ್ ಓದಲಾಗಲಿಲ್ಲ.",
        "observation_error": "ವೀಕ್ಷಣೆಯನ್ನು ಉಳಿಸಲಾಗಲಿಲ್ಲ.",
        "original": "ಮೂಲ ಮಾದರಿಯ ವಿಶ್ವಾಸ ಮಟ್ಟ",
    },
    "ml": {
        "title": "📔 വിള ആരോഗ്യ ഡയറി",
        "intro": "വിളയുടെ രോഗനിർണയം സൂക്ഷിക്കുകയും കാലക്രമത്തിലുള്ള മാറ്റങ്ങൾ രേഖപ്പെടുത്തുകയും ചെയ്യുക.",
        "save": "➕ നിലവിലെ രോഗനിർണയം സൂക്ഷിക്കുക",
        "crop": "വിള",
        "condition": "പ്രവചിച്ച രോഗം",
        "confidence": "മോഡലിന്റെ വിശ്വാസനില",
        "confidence_note": "ഇത് മോഡലിന്റെ കണക്കുകൂട്ടലാണ്; കൃത്യതയ്ക്കുള്ള ഉറപ്പല്ല.",
        "symptoms": "ശ്രദ്ധയിൽപ്പെട്ട ലക്ഷണങ്ങൾ (ഐച്ഛികം)",
        "symptoms_hint": "ഉദാ. ഇലയുടെ അരികുകളിൽ തവിട്ടുനിറത്തിലുള്ള പാടുകൾ",
        "save_button": "വിള ഡയറിയിൽ സൂക്ഷിക്കുക",
        "saved": "രോഗനിർണയം ഡയറിയിൽ സൂക്ഷിച്ചു!",
        "save_error": "രേഖ സൂക്ഷിക്കാനായില്ല. ഫോൾഡർ അനുമതികൾ പരിശോധിക്കുക.",
        "history": "നിങ്ങളുടെ വിളയുടെ ചരിത്രം",
        "empty": "ഡയറി ശൂന്യമാണ്. ഇല പരിശോധിച്ച് രേഖ സൂക്ഷിക്കുക.",
        "entries": "സൂക്ഷിച്ച രേഖകൾ",
        "recorded": "രേഖപ്പെടുത്തിയ തീയതി",
        "photo": "സൂക്ഷിച്ച ഇലയുടെ ചിത്രം",
        "initial": "ആദ്യ ലക്ഷണങ്ങൾ",
        "alternatives": "മോഡലിന്റെ മറ്റ് പ്രവചനങ്ങൾ",
        "timeline": "തുടർ നിരീക്ഷണങ്ങൾ",
        "no_observations": "ഇതുവരെ തുടർ നിരീക്ഷണങ്ങൾ ഇല്ല.",
        "current": "ഇപ്പോൾ ചെടി എങ്ങനെയുണ്ട്?",
        "unchanged": "വ്യക്തമായ മാറ്റമില്ല",
        "improved": "ലക്ഷണങ്ങൾ മെച്ചപ്പെട്ടതായി തോന്നുന്നു",
        "worse": "ലക്ഷണങ്ങൾ കൂടുന്നതായി തോന്നുന്നു",
        "new": "പുതിയ ലക്ഷണങ്ങൾ കണ്ടു",
        "notes": "ഇന്നത്തെ നിരീക്ഷണങ്ങൾ (ഐച്ഛികം)",
        "notes_hint": "ഇന്ന് ശ്രദ്ധിച്ച കാര്യങ്ങൾ എഴുതുക...",
        "add": "നിരീക്ഷണം ചേർക്കുക",
        "added": "നിരീക്ഷണം ചേർത്തു!",
        "missing": "ഈ രേഖ കണ്ടെത്താനായില്ല.",
        "read_error": "ഡയറി ഫയൽ വായിക്കാനായില്ല.",
        "observation_error": "നിരീക്ഷണം സൂക്ഷിക്കാനായില്ല.",
        "original": "യഥാർത്ഥ മോഡലിന്റെ വിശ്വാസനില",
    },
}


def _prepare_storage():
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    if not JOURNAL_FILE.exists():
        JOURNAL_FILE.write_text("[]", encoding="utf-8")


def _load_entries():
    _prepare_storage()
    try:
        data = json.loads(JOURNAL_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        st.error("The journal file could not be read. Please check its contents.")
        return []


def _save_entries(entries):
    _prepare_storage()
    temporary = JOURNAL_FILE.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary.replace(JOURNAL_FILE)


def render_journal(crop=None, photo_bytes=None, lang_code="en"):
    t = TEXT.get(lang_code, TEXT["en"])

    st.header(t["title"])
    st.caption(t["intro"])

    if crop and photo_bytes:
        with st.expander(t["save"], expanded=False):
            st.write(f"**{t['crop']}:** {crop['crop']}")
            st.write(f"**{t['condition']}:** {crop['condition']}")
            st.write(
                f"**{t['confidence']}:** "
                f"{crop['confidence'] * 100:.1f}%"
            )
            st.caption(t["confidence_note"])

            with st.form("save_crop_diagnosis_form"):
                symptoms = st.text_area(
                    t["symptoms"],
                    placeholder=t["symptoms_hint"],
                )
                submitted = st.form_submit_button(
                    t["save_button"],
                    type="primary",
                )

            if submitted:
                entries = _load_entries()
                entry_id = uuid.uuid4().hex
                now = datetime.now().astimezone().isoformat(
                    timespec="seconds"
                )
                image_path = IMAGE_DIR / f"{entry_id}.jpg"

                try:
                    image_path.write_bytes(photo_bytes)
                    entry = {
                        "id": entry_id,
                        "date": now,
                        "crop": crop["crop"],
                        "condition": crop["condition"],
                        "label": crop.get("label", ""),
                        "confidence": float(crop["confidence"]),
                        "alternatives": [
                            [name, condition, float(probability)]
                            for name, condition, probability
                            in crop.get("alternatives", [])
                        ],
                        "symptoms": symptoms.strip(),
                        "image": str(image_path.relative_to(BASE_DIR)),
                        "observations": [],
                    }
                    entries.insert(0, entry)
                    _save_entries(entries)
                    st.success(t["saved"])
                    st.rerun()
                except OSError:
                    st.error(t["save_error"])

    entries = _load_entries()
    st.subheader(t["history"])

    if not entries:
        st.info(t["empty"])
        return

    st.caption(f"{len(entries)} {t['entries']}")

    status_values = [
        t["unchanged"],
        t["improved"],
        t["worse"],
        t["new"],
    ]

    for entry in entries:
        title = (
            f"{entry.get('crop', 'Unknown')} — "
            f"{entry.get('condition', 'Unknown')}"
        )
        with st.expander(title):
            st.caption(f"{t['recorded']}: {entry.get('date', '—')}")

            image_path = BASE_DIR / entry.get("image", "")
            if image_path.is_file():
                st.image(str(image_path), caption=t["photo"], width=260)

            st.write(
                f"**{t['original']}:** "
                f"{entry.get('confidence', 0) * 100:.1f}%"
            )

            if entry.get("symptoms"):
                st.write(f"**{t['initial']}:** {entry['symptoms']}")

            alternatives = entry.get("alternatives", [])
            if alternatives:
                st.write(f"**{t['alternatives']}:**")
                for name, condition, probability in alternatives:
                    st.write(
                        f"- {name} — {condition}: "
                        f"{probability * 100:.1f}%"
                    )

            st.write(f"**{t['timeline']}**")
            observations = entry.get("observations", [])

            if observations:
                for observation in observations:
                    st.markdown(
                        f"- **{observation['date']}** — "
                        f"{observation['status']}"
                    )
                    if observation.get("note"):
                        st.write(observation["note"])
            else:
                st.caption(t["no_observations"])

            with st.form(f"observation_form_{entry['id']}"):
                status = st.selectbox(
                    t["current"],
                    status_values,
                    key=f"status_{entry['id']}_{lang_code}",
                )
                note = st.text_area(
                    t["notes"],
                    placeholder=t["notes_hint"],
                    key=f"note_{entry['id']}_{lang_code}",
                )
                add_observation = st.form_submit_button(t["add"])

            if add_observation:
                latest_entries = _load_entries()
                target = next(
                    (
                        item for item in latest_entries
                        if item.get("id") == entry["id"]
                    ),
                    None,
                )

                if target is None:
                    st.error(t["missing"])
                else:
                    status_key = status_values.index(status)
                    status_codes = [
                        "No visible change",
                        "Symptoms appear improved",
                        "Symptoms appear worse",
                        "New symptoms noticed",
                    ]
                    target.setdefault("observations", []).append({
                        "date": datetime.now().astimezone().isoformat(
                            timespec="seconds"
                        ),
                        "status": status_codes[status_key],
                        "note": note.strip(),
                    })
                    try:
                        _save_entries(latest_entries)
                        st.success(t["added"])
                        st.rerun()
                    except OSError:
                        st.error(t["observation_error"])
