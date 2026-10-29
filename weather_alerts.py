"""Weather-based crop disease risk alerts for KisanMitra."""

import requests
import streamlit as st

from agri_risk import assess_weather_risk

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT = 15

WEATHER_TEXT = {
    "English": {
        "title": "🌦️ Weather-Based Disease Alerts",
        "intro": "Check upcoming weather conditions that may favor selected crop diseases.",
        "place": "Enter city, district or town",
        "crop": "Enter your crop",
        "find": "Find locations",
        "searching": "Searching for locations...",
        "empty": "Please enter a location first.",
        "none": "No matching Indian locations found. Try another spelling or a nearby city.",
        "search_error": "Could not search for locations. Check your internet connection and try again.",
        "choose": "Select your location",
        "no_locations": "Enter a location and click Find locations to see matching places.",
        "forecasting": "Fetching weather forecast...",
        "forecast_error": "Could not load the forecast for this location. Please try again.",
        "retry": "Retry forecast",
        "forecast_heading": "Forecast location:",
        "three_day": "Three-day forecast",
        "date": "Date",
        "min": "Min °C",
        "max": "Max °C",
        "rain": "Rain (mm)",
        "assessment": "AI crop disease risk assessment",
        "guidance": "Read disease guidance",
        "no_risk": "No specific disease risk was identified from the retrieved evidence. This does not mean the crop is disease-free.",
        "disclaimer": "AI-generated screening based on retrieved agricultural information and forecast data. This is not a confirmed diagnosis or an official agricultural warning. Verify important decisions with your local Krishi Vigyan Kendra (KVK) or agricultural officer.",
        "watch": "Watch",
        "elevated": "Elevated",
        "insufficient": "Insufficient evidence",
        "example": "e.g. Karnal, Haryana",
        "crop_example": "e.g. Apple, Maize, Rice, Wheat",
    },
    "Hindi": {
        "title": "🌦️ मौसम-आधारित फसल रोग चेतावनी",
        "intro": "आने वाले मौसम की जाँच करें, जो फसल में कुछ रोगों के अनुकूल हो सकता है।",
        "place": "शहर, ज़िला या कस्बा दर्ज करें",
        "crop": "अपनी फसल का नाम दर्ज करें",
        "find": "स्थान खोजें",
        "searching": "स्थान खोजे जा रहे हैं...",
        "empty": "कृपया पहले स्थान दर्ज करें।",
        "none": "भारत में इस नाम का स्थान नहीं मिला। वर्तनी बदलकर या पास के शहर का नाम डालकर देखें।",
        "search_error": "स्थान नहीं खोजा जा सका। इंटरनेट जाँचकर फिर प्रयास करें।",
        "choose": "अपना स्थान चुनें",
        "no_locations": "स्थान दर्ज करें और मिलते-जुलते स्थान देखने के लिए 'स्थान खोजें' पर क्लिक करें।",
        "forecasting": "मौसम का पूर्वानुमान प्राप्त हो रहा है...",
        "forecast_error": "इस स्थान का मौसम पूर्वानुमान नहीं मिल सका। कृपया फिर प्रयास करें।",
        "retry": "पूर्वानुमान फिर से प्राप्त करें",
        "forecast_heading": "पूर्वानुमान का स्थान:",
        "three_day": "तीन दिन का पूर्वानुमान",
        "date": "तारीख",
        "min": "न्यूनतम °C",
        "max": "अधिकतम °C",
        "rain": "बारिश (मिमी)",
        "assessment": "AI द्वारा फसल रोग जोखिम आकलन",
        "guidance": "रोग संबंधी जानकारी पढ़ें",
        "no_risk": "प्राप्त जानकारी से किसी विशेष रोग का जोखिम नहीं मिला। इसका अर्थ यह नहीं है कि फसल रोग-मुक्त है।",
        "disclaimer": "यह प्राप्त कृषि जानकारी और मौसम पूर्वानुमान पर आधारित AI जाँच है। यह पक्की बीमारी की पहचान या आधिकारिक कृषि चेतावनी नहीं है। महत्वपूर्ण निर्णय के लिए स्थानीय कृषि विज्ञान केंद्र (KVK) या कृषि अधिकारी से सलाह लें।",
        "watch": "नज़र रखें",
        "elevated": "बढ़ा हुआ जोखिम",
        "insufficient": "पर्याप्त जानकारी नहीं",
        "example": "जैसे: करनाल, हरियाणा",
        "crop_example": "जैसे: सेब, मक्का, चावल, गेहूँ",
    },
    "Punjabi": {
        "title": "🌦️ ਮੌਸਮ-ਅਧਾਰਿਤ ਫ਼ਸਲ ਰੋਗ ਚੇਤਾਵਨੀਆਂ",
        "intro": "ਆਉਣ ਵਾਲੇ ਮੌਸਮ ਦੀ ਜਾਂਚ ਕਰੋ, ਜੋ ਕੁਝ ਫ਼ਸਲੀ ਬਿਮਾਰੀਆਂ ਲਈ ਅਨੁਕੂਲ ਹੋ ਸਕਦਾ ਹੈ।",
        "place": "ਸ਼ਹਿਰ, ਜ਼ਿਲ੍ਹਾ ਜਾਂ ਕਸਬਾ ਦਰਜ ਕਰੋ",
        "crop": "ਆਪਣੀ ਫ਼ਸਲ ਦਾ ਨਾਮ ਦਰਜ ਕਰੋ",
        "find": "ਥਾਂਵਾਂ ਲੱਭੋ",
        "searching": "ਥਾਂਵਾਂ ਲੱਭੀਆਂ ਜਾ ਰਹੀਆਂ ਹਨ...",
        "empty": "ਪਹਿਲਾਂ ਕੋਈ ਥਾਂ ਦਰਜ ਕਰੋ।",
        "none": "ਭਾਰਤ ਵਿੱਚ ਇਸ ਨਾਮ ਦੀ ਥਾਂ ਨਹੀਂ ਮਿਲੀ। ਸਪੈਲਿੰਗ ਬਦਲ ਕੇ ਜਾਂ ਨੇੜਲੇ ਸ਼ਹਿਰ ਦਾ ਨਾਮ ਅਜ਼ਮਾਓ।",
        "search_error": "ਥਾਂਵਾਂ ਨਹੀਂ ਲੱਭੀਆਂ ਜਾ ਸਕੀਆਂ। ਇੰਟਰਨੈੱਟ ਜਾਂਚ ਕੇ ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।",
        "choose": "ਆਪਣੀ ਥਾਂ ਚੁਣੋ",
        "no_locations": "ਥਾਂ ਦਰਜ ਕਰੋ ਅਤੇ ਮਿਲਦੀਆਂ ਥਾਂਵਾਂ ਦੇਖਣ ਲਈ 'ਥਾਂਵਾਂ ਲੱਭੋ' ਦਬਾਓ।",
        "forecasting": "ਮੌਸਮ ਦੀ ਭਵਿੱਖਬਾਣੀ ਲਈ ਜਾ ਰਹੀ ਹੈ...",
        "forecast_error": "ਇਸ ਥਾਂ ਲਈ ਮੌਸਮ ਦੀ ਭਵਿੱਖਬਾਣੀ ਨਹੀਂ ਮਿਲੀ। ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।",
        "retry": "ਭਵਿੱਖਬਾਣੀ ਦੁਬਾਰਾ ਲਵੋ",
        "forecast_heading": "ਭਵਿੱਖਬਾਣੀ ਵਾਲੀ ਥਾਂ:",
        "three_day": "ਤਿੰਨ ਦਿਨਾਂ ਦੀ ਭਵਿੱਖਬਾਣੀ",
        "date": "ਤਾਰੀਖ",
        "min": "ਘੱਟੋ-ਘੱਟ °C",
        "max": "ਵੱਧ ਤੋਂ ਵੱਧ °C",
        "rain": "ਮੀਂਹ (ਮਿ.ਮੀ.)",
        "assessment": "AI ਫ਼ਸਲ ਰੋਗ ਜੋਖਮ ਮੁਲਾਂਕਣ",
        "guidance": "ਰੋਗ ਬਾਰੇ ਜਾਣਕਾਰੀ ਪੜ੍ਹੋ",
        "no_risk": "ਮਿਲੀ ਜਾਣਕਾਰੀ ਤੋਂ ਕਿਸੇ ਖਾਸ ਰੋਗ ਦਾ ਜੋਖਮ ਨਹੀਂ ਮਿਲਿਆ। ਇਸਦਾ ਮਤਲਬ ਇਹ ਨਹੀਂ ਕਿ ਫ਼ਸਲ ਬਿਮਾਰੀ-ਮੁਕਤ ਹੈ।",
        "disclaimer": "ਇਹ ਖੇਤੀਬਾੜੀ ਜਾਣਕਾਰੀ ਅਤੇ ਮੌਸਮ ਦੀ ਭਵਿੱਖਬਾਣੀ 'ਤੇ ਆਧਾਰਿਤ AI ਜਾਂਚ ਹੈ। ਇਹ ਪੱਕੀ ਤਸ਼ਖ਼ੀਸ ਜਾਂ ਸਰਕਾਰੀ ਖੇਤੀਬਾੜੀ ਚੇਤਾਵਨੀ ਨਹੀਂ ਹੈ। ਮਹੱਤਵਪੂਰਨ ਫ਼ੈਸਲਿਆਂ ਲਈ ਆਪਣੇ ਕ੍ਰਿਸ਼ੀ ਵਿਗਿਆਨ ਕੇਂਦਰ (KVK) ਜਾਂ ਖੇਤੀਬਾੜੀ ਅਧਿਕਾਰੀ ਨਾਲ ਸਲਾਹ ਕਰੋ।",
        "watch": "ਨਜ਼ਰ ਰੱਖੋ",
        "elevated": "ਵਧਿਆ ਹੋਇਆ ਜੋਖਮ",
        "insufficient": "ਲੋੜੀਂਦੇ ਸਬੂਤ ਨਹੀਂ",
        "example": "ਜਿਵੇਂ: ਕਰਨਾਲ, ਹਰਿਆਣਾ",
        "crop_example": "ਜਿਵੇਂ: ਸੇਬ, ਮੱਕੀ, ਚੌਲ, ਕਣਕ",
    },
    "Marathi": {
        "title": "🌦️ हवामानावर आधारित पीक रोग सूचना",
        "intro": "पिकांच्या काही रोगांना अनुकूल ठरू शकणाऱ्या आगामी हवामानाची माहिती तपासा.",
        "place": "शहर, जिल्हा किंवा गावाचे नाव टाका",
        "crop": "पिकाचे नाव टाका",
        "find": "ठिकाणे शोधा",
        "searching": "ठिकाणे शोधत आहोत...",
        "empty": "कृपया आधी ठिकाणाचे नाव टाका.",
        "none": "भारतात या नावाचे ठिकाण सापडले नाही. स्पेलिंग किंवा जवळच्या शहराचे नाव वापरून पाहा.",
        "search_error": "ठिकाण शोधता आले नाही. इंटरनेट तपासून पुन्हा प्रयत्न करा.",
        "choose": "तुमचे ठिकाण निवडा",
        "no_locations": "ठिकाण टाकून जुळणारी ठिकाणे पाहण्यासाठी 'ठिकाणे शोधा' निवडा.",
        "forecasting": "हवामानाचा अंदाज मिळवत आहोत...",
        "forecast_error": "या ठिकाणाचा हवामान अंदाज मिळाला नाही. पुन्हा प्रयत्न करा.",
        "retry": "अंदाज पुन्हा मिळवा",
        "forecast_heading": "अंदाजाचे ठिकाण:",
        "three_day": "तीन दिवसांचा अंदाज",
        "date": "तारीख",
        "min": "किमान °C",
        "max": "कमाल °C",
        "rain": "पाऊस (मिमी)",
        "assessment": "AI पीक रोग जोखीम मूल्यांकन",
        "guidance": "रोगाविषयी मार्गदर्शन वाचा",
        "no_risk": "मिळालेल्या माहितीतून विशिष्ट रोगाचा धोका आढळला नाही. याचा अर्थ पीक रोगमुक्त आहे असे नाही.",
        "disclaimer": "ही उपलब्ध कृषी माहिती आणि हवामानाच्या अंदाजावर आधारित AI तपासणी आहे. हे निश्चित निदान किंवा अधिकृत कृषी इशारा नाही. महत्त्वाच्या निर्णयांसाठी स्थानिक कृषी विज्ञान केंद्र (KVK) किंवा कृषी अधिकाऱ्यांचा सल्ला घ्या.",
        "watch": "लक्ष ठेवा",
        "elevated": "वाढलेला धोका",
        "insufficient": "पुरेसा पुरावा नाही",
        "example": "उदा. कर्नाल, हरियाणा",
        "crop_example": "उदा. सफरचंद, मका, तांदूळ, गहू",
    },
    "Gujarati": {
        "title": "🌦️ હવામાન આધારિત પાક રોગ ચેતવણીઓ",
        "intro": "પાકના કેટલાક રોગોને અનુકૂળ બની શકે તેવી આગામી હવામાનની સ્થિતિ તપાસો.",
        "place": "શહેર, જિલ્લો અથવા ગામનું નામ દાખલ કરો",
        "crop": "તમારા પાકનું નામ દાખલ કરો",
        "find": "સ્થળો શોધો",
        "searching": "સ્થળો શોધાઈ રહ્યાં છે...",
        "empty": "કૃપા કરીને પહેલાં સ્થળ દાખલ કરો.",
        "none": "ભારતમાં આ નામનું સ્થળ મળ્યું નથી. જોડણી અથવા નજીકના શહેરનું નામ અજમાવો.",
        "search_error": "સ્થળ શોધી શકાયું નથી. ઇન્ટરનેટ તપાસીને ફરી પ્રયાસ કરો.",
        "choose": "તમારું સ્થળ પસંદ કરો",
        "no_locations": "સ્થળ દાખલ કરો અને મેળ ખાતાં સ્થળો જોવા 'સ્થળો શોધો' પસંદ કરો.",
        "forecasting": "હવામાનની આગાહી મેળવી રહ્યાં છીએ...",
        "forecast_error": "આ સ્થળની હવામાન આગાહી મળી શકી નથી. ફરી પ્રયાસ કરો.",
        "retry": "આગાહી ફરી મેળવો",
        "forecast_heading": "આગાહીનું સ્થળ:",
        "three_day": "ત્રણ દિવસની આગાહી",
        "date": "તારીખ",
        "min": "લઘુત્તમ °C",
        "max": "મહત્તમ °C",
        "rain": "વરસાદ (મિમી)",
        "assessment": "AI પાક રોગ જોખમ મૂલ્યાંકન",
        "guidance": "રોગ વિશે માર્ગદર્શન વાંચો",
        "no_risk": "મળેલી માહિતીમાં કોઈ ચોક્કસ રોગનું જોખમ ઓળખાયું નથી. તેનો અર્થ પાક રોગમુક્ત છે એવો નથી.",
        "disclaimer": "આ ખેતી સંબંધિત માહિતી અને હવામાનની આગાહી પર આધારિત AI તપાસ છે. આ નિશ્ચિત નિદાન કે સત્તાવાર કૃષિ ચેતવણી નથી. મહત્ત્વના નિર્ણયો માટે સ્થાનિક કૃષિ વિજ્ઞાન કેન્દ્ર (KVK) અથવા કૃષિ અધિકારીની સલાહ લો.",
        "watch": "ધ્યાન રાખો",
        "elevated": "વધેલું જોખમ",
        "insufficient": "પૂરતા પુરાવા નથી",
        "example": "દા.ત. કરનાલ, હરિયાણા",
        "crop_example": "દા.ત. સફરજન, મકાઈ, ચોખા, ઘઉં",
    },
    "Bengali": {
        "title": "🌦️ আবহাওয়াভিত্তিক ফসলের রোগ সতর্কতা",
        "intro": "ফসলের কিছু রোগের অনুকূল হতে পারে এমন আসন্ন আবহাওয়ার পরিস্থিতি দেখুন।",
        "place": "শহর, জেলা বা গ্রামের নাম লিখুন",
        "crop": "আপনার ফসলের নাম লিখুন",
        "find": "স্থান খুঁজুন",
        "searching": "স্থান খোঁজা হচ্ছে...",
        "empty": "অনুগ্রহ করে আগে একটি স্থানের নাম লিখুন।",
        "none": "ভারতে এই নামে কোনো স্থান পাওয়া যায়নি। বানান বদলে বা কাছের শহরের নাম দিয়ে চেষ্টা করুন।",
        "search_error": "স্থান খোঁজা যায়নি। ইন্টারনেট পরীক্ষা করে আবার চেষ্টা করুন।",
        "choose": "আপনার স্থান নির্বাচন করুন",
        "no_locations": "স্থান লিখে মিল থাকা স্থান দেখতে 'স্থান খুঁজুন' নির্বাচন করুন।",
        "forecasting": "আবহাওয়ার পূর্বাভাস আনা হচ্ছে...",
        "forecast_error": "এই স্থানের আবহাওয়ার পূর্বাভাস পাওয়া যায়নি। আবার চেষ্টা করুন।",
        "retry": "পূর্বাভাস আবার দেখুন",
        "forecast_heading": "পূর্বাভাসের স্থান:",
        "three_day": "তিন দিনের পূর্বাভাস",
        "date": "তারিখ",
        "min": "সর্বনিম্ন °C",
        "max": "সর্বোচ্চ °C",
        "rain": "বৃষ্টি (মিমি)",
        "assessment": "AI ফসলের রোগের ঝুঁকি মূল্যায়ন",
        "guidance": "রোগের নির্দেশিকা পড়ুন",
        "no_risk": "প্রাপ্ত তথ্য থেকে নির্দিষ্ট কোনো রোগের ঝুঁকি শনাক্ত হয়নি। এর অর্থ এই নয় যে ফসল রোগমুক্ত।",
        "disclaimer": "এটি প্রাপ্ত কৃষি-তথ্য ও আবহাওয়ার পূর্বাভাসের ভিত্তিতে AI-পরীক্ষা। এটি নিশ্চিত রোগনির্ণয় বা সরকারি কৃষি সতর্কতা নয়। গুরুত্বপূর্ণ সিদ্ধান্তের আগে স্থানীয় কৃষি বিজ্ঞান কেন্দ্র (KVK) বা কৃষি আধিকারিকের পরামর্শ নিন।",
        "watch": "নজর রাখুন",
        "elevated": "বর্ধিত ঝুঁকি",
        "insufficient": "পর্যাপ্ত প্রমাণ নেই",
        "example": "যেমন: কর্নাল, হরিয়ানা",
        "crop_example": "যেমন: আপেল, ভুট্টা, ধান, গম",
    },
    "Tamil": {
        "title": "🌦️ வானிலை சார்ந்த பயிர் நோய் எச்சரிக்கைகள்",
        "intro": "பயிர் நோய்களுக்கு சாதகமாக இருக்கக்கூடிய வரவிருக்கும் வானிலையைப் பாருங்கள்.",
        "place": "நகரம், மாவட்டம் அல்லது ஊரின் பெயரை உள்ளிடவும்",
        "crop": "பயிரின் பெயரை உள்ளிடவும்",
        "find": "இடங்களைக் கண்டறியவும்",
        "searching": "இடங்களைத் தேடுகிறது...",
        "empty": "முதலில் ஓர் இடத்தின் பெயரை உள்ளிடவும்.",
        "none": "இந்தியாவில் பொருந்தும் இடம் கிடைக்கவில்லை. எழுத்துப்பிழையை மாற்றி அல்லது அருகிலுள்ள நகரத்தை முயற்சிக்கவும்.",
        "search_error": "இடங்களைத் தேட முடியவில்லை. இணைய இணைப்பைச் சரிபார்த்து மீண்டும் முயற்சிக்கவும்.",
        "choose": "உங்கள் இடத்தைத் தேர்ந்தெடுக்கவும்",
        "no_locations": "இடத்தை உள்ளிட்டு, பொருந்தும் இடங்களைக் காண 'இடங்களைக் கண்டறியவும்' என்பதைத் தேர்ந்தெடுக்கவும்.",
        "forecasting": "வானிலை முன்னறிவிப்பைப் பெறுகிறது...",
        "forecast_error": "இந்த இடத்திற்கான வானிலை முன்னறிவிப்பைப் பெற முடியவில்லை. மீண்டும் முயற்சிக்கவும்.",
        "retry": "முன்னறிவிப்பை மீண்டும் பெறவும்",
        "forecast_heading": "முன்னறிவிப்பு இடம்:",
        "three_day": "மூன்று நாள் முன்னறிவிப்பு",
        "date": "தேதி",
        "min": "குறைந்தபட்சம் °C",
        "max": "அதிகபட்சம் °C",
        "rain": "மழை (மிமீ)",
        "assessment": "AI பயிர் நோய் அபாய மதிப்பீடு",
        "guidance": "நோய் வழிகாட்டியைப் படிக்கவும்",
        "no_risk": "கிடைத்த தகவலில் குறிப்பிட்ட நோய் அபாயம் கண்டறியப்படவில்லை. இதனால் பயிர் நோயற்றது என்று அர்த்தமில்லை.",
        "disclaimer": "இது பெறப்பட்ட வேளாண் தகவல் மற்றும் வானிலை முன்னறிவிப்பின் அடிப்படையிலான AI மதிப்பீடு. இது உறுதியான நோயறிதலோ அதிகாரப்பூர்வ வேளாண் எச்சரிக்கையோ அல்ல. முக்கிய முடிவுகளுக்கு உள்ளூர் கிருஷி விஞ்ஞான் கேந்திரா (KVK) அல்லது வேளாண் அதிகாரியிடம் ஆலோசனை பெறவும்.",
        "watch": "கவனிக்கவும்",
        "elevated": "அதிகரித்த அபாயம்",
        "insufficient": "போதிய ஆதாரம் இல்லை",
        "example": "எ.கா. கர்னால், ஹரியானா",
        "crop_example": "எ.கா. ஆப்பிள், மக்காச்சோளம், அரிசி, கோதுமை",
    },
    "Telugu": {
        "title": "🌦️ వాతావరణ ఆధారిత పంట వ్యాధి హెచ్చరికలు",
        "intro": "పంట వ్యాధులకు అనుకూలంగా ఉండే అవకాశం ఉన్న రాబోయే వాతావరణ పరిస్థితులను పరిశీలించండి.",
        "place": "నగరం, జిల్లా లేదా పట్టణం పేరు నమోదు చేయండి",
        "crop": "మీ పంట పేరు నమోదు చేయండి",
        "find": "ప్రాంతాలను వెతకండి",
        "searching": "ప్రాంతాలను వెతుకుతోంది...",
        "empty": "దయచేసి ముందుగా ఒక ప్రాంతం పేరు నమోదు చేయండి.",
        "none": "భారతదేశంలో సరిపోలే ప్రాంతం కనబడలేదు. అక్షరక్రమాన్ని మార్చి లేదా సమీప నగరాన్ని ప్రయత్నించండి.",
        "search_error": "ప్రాంతాలను వెతకలేకపోయాం. ఇంటర్నెట్‌ను తనిఖీ చేసి మళ్లీ ప్రయత్నించండి.",
        "choose": "మీ ప్రాంతాన్ని ఎంచుకోండి",
        "no_locations": "ప్రాంతం పేరు నమోదు చేసి, సరిపోలే ప్రాంతాలను చూడటానికి 'ప్రాంతాలను వెతకండి' ఎంచుకోండి.",
        "forecasting": "వాతావరణ అంచనాను పొందుతోంది...",
        "forecast_error": "ఈ ప్రాంతానికి వాతావరణ అంచనా అందలేదు. మళ్లీ ప్రయత్నించండి.",
        "retry": "అంచనాను మళ్లీ పొందండి",
        "forecast_heading": "అంచనా ప్రాంతం:",
        "three_day": "మూడు రోజుల అంచనా",
        "date": "తేదీ",
        "min": "కనిష్ఠం °C",
        "max": "గరిష్ఠం °C",
        "rain": "వర్షం (మి.మీ.)",
        "assessment": "AI పంట వ్యాధి ప్రమాద అంచనా",
        "guidance": "వ్యాధి మార్గదర్శకాన్ని చదవండి",
        "no_risk": "లభించిన ఆధారాల్లో నిర్దిష్ట వ్యాధి ప్రమాదం గుర్తించబడలేదు. దీనర్థం పంటకు వ్యాధి లేదని కాదు.",
        "disclaimer": "ఇది సేకరించిన వ్యవసాయ సమాచారం మరియు వాతావరణ అంచనాల ఆధారంగా రూపొందించిన AI పరిశీలన మాత్రమే. ఇది నిర్ధారిత రోగనిర్ధారణ లేదా అధికారిక వ్యవసాయ హెచ్చరిక కాదు. ముఖ్యమైన నిర్ణయాల కోసం స్థానిక కృషి విజ్ఞాన కేంద్రం (KVK) లేదా వ్యవసాయ అధికారిని సంప్రదించండి.",
        "watch": "గమనించండి",
        "elevated": "పెరిగిన ప్రమాదం",
        "insufficient": "తగిన ఆధారాలు లేవు",
        "example": "ఉదా. కర్నాల్, హర్యానా",
        "crop_example": "ఉదా. ఆపిల్, మొక్కజొన్న, వరి, గోధుమ",
    },
    "Kannada": {
        "title": "🌦️ ಹವಾಮಾನ ಆಧಾರಿತ ಬೆಳೆ ರೋಗ ಎಚ್ಚರಿಕೆಗಳು",
        "intro": "ಬೆಳೆ ರೋಗಗಳಿಗೆ ಅನುಕೂಲವಾಗಬಹುದಾದ ಮುಂಬರುವ ಹವಾಮಾನ ಪರಿಸ್ಥಿತಿಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "place": "ನಗರ, ಜಿಲ್ಲೆ ಅಥವಾ ಊರಿನ ಹೆಸರನ್ನು ನಮೂದಿಸಿ",
        "crop": "ನಿಮ್ಮ ಬೆಳೆಯ ಹೆಸರನ್ನು ನಮೂದಿಸಿ",
        "find": "ಸ್ಥಳಗಳನ್ನು ಹುಡುಕಿ",
        "searching": "ಸ್ಥಳಗಳನ್ನು ಹುಡುಕಲಾಗುತ್ತಿದೆ...",
        "empty": "ದಯವಿಟ್ಟು ಮೊದಲು ಸ್ಥಳದ ಹೆಸರನ್ನು ನಮೂದಿಸಿ.",
        "none": "ಭಾರತದಲ್ಲಿ ಹೊಂದುವ ಸ್ಥಳ ಕಂಡುಬಂದಿಲ್ಲ. ಕಾಗುಣಿತ ಬದಲಿಸಿ ಅಥವಾ ಹತ್ತಿರದ ನಗರದ ಹೆಸರನ್ನು ಪ್ರಯತ್ನಿಸಿ.",
        "search_error": "ಸ್ಥಳಗಳನ್ನು ಹುಡುಕಲಾಗಲಿಲ್ಲ. ಇಂಟರ್ನೆಟ್ ಪರಿಶೀಲಿಸಿ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "choose": "ನಿಮ್ಮ ಸ್ಥಳವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "no_locations": "ಸ್ಥಳದ ಹೆಸರನ್ನು ನಮೂದಿಸಿ, ಹೊಂದುವ ಸ್ಥಳಗಳನ್ನು ನೋಡಲು 'ಸ್ಥಳಗಳನ್ನು ಹುಡುಕಿ' ಆಯ್ಕೆಮಾಡಿ.",
        "forecasting": "ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ ಪಡೆಯಲಾಗುತ್ತಿದೆ...",
        "forecast_error": "ಈ ಸ್ಥಳದ ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ ಸಿಗಲಿಲ್ಲ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "retry": "ಮುನ್ಸೂಚನೆಯನ್ನು ಮತ್ತೆ ಪಡೆಯಿರಿ",
        "forecast_heading": "ಮುನ್ಸೂಚನೆಯ ಸ್ಥಳ:",
        "three_day": "ಮೂರು ದಿನಗಳ ಮುನ್ಸೂಚನೆ",
        "date": "ದಿನಾಂಕ",
        "min": "ಕನಿಷ್ಠ °C",
        "max": "ಗರಿಷ್ಠ °C",
        "rain": "ಮಳೆ (ಮಿಮೀ)",
        "assessment": "AI ಬೆಳೆ ರೋಗದ ಅಪಾಯ ಮೌಲ್ಯಮಾಪನ",
        "guidance": "ರೋಗದ ಮಾರ್ಗದರ್ಶನ ಓದಿ",
        "no_risk": "ಲಭ್ಯವಿರುವ ಮಾಹಿತಿಯಿಂದ ನಿರ್ದಿಷ್ಟ ರೋಗದ ಅಪಾಯ ಕಂಡುಬಂದಿಲ್ಲ. ಇದರಿಂದ ಬೆಳೆ ರೋಗಮುಕ್ತವಾಗಿದೆ ಎಂದರ್ಥವಲ್ಲ.",
        "disclaimer": "ಇದು ಲಭ್ಯ ಕೃಷಿ ಮಾಹಿತಿ ಮತ್ತು ಹವಾಮಾನ ಮುನ್ಸೂಚನೆಯ ಆಧಾರದ AI ಪರಿಶೀಲನೆ. ಇದು ಖಚಿತ ರೋಗನಿರ್ಣಯ ಅಥವಾ ಅಧಿಕೃತ ಕೃಷಿ ಎಚ್ಚರಿಕೆ ಅಲ್ಲ. ಪ್ರಮುಖ ನಿರ್ಧಾರಗಳಿಗಾಗಿ ಸ್ಥಳೀಯ ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರ (KVK) ಅಥವಾ ಕೃಷಿ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        "watch": "ಗಮನಿಸಿ",
        "elevated": "ಹೆಚ್ಚಿದ ಅಪಾಯ",
        "insufficient": "ಸಾಕಷ್ಟು ಸಾಕ್ಷ್ಯವಿಲ್ಲ",
        "example": "ಉದಾ. ಕರ್ನಾಲ್, ಹರಿಯಾಣ",
        "crop_example": "ಉದಾ. ಸೇಬು, ಜೋಳ, ಅಕ್ಕಿ, ಗೋಧಿ",
    },
    "Malayalam": {
        "title": "🌦️ കാലാവസ്ഥയെ അടിസ്ഥാനമാക്കിയുള്ള വിളരോഗ മുന്നറിയിപ്പുകൾ",
        "intro": "വിളരോഗങ്ങൾക്ക് അനുകൂലമായേക്കാവുന്ന വരാനിരിക്കുന്ന കാലാവസ്ഥ പരിശോധിക്കുക.",
        "place": "നഗരം, ജില്ല അല്ലെങ്കിൽ ഗ്രാമത്തിന്റെ പേര് നൽകുക",
        "crop": "നിങ്ങളുടെ വിളയുടെ പേര് നൽകുക",
        "find": "സ്ഥലങ്ങൾ കണ്ടെത്തുക",
        "searching": "സ്ഥലങ്ങൾ തിരയുന്നു...",
        "empty": "ദയവായി ആദ്യം ഒരു സ്ഥലത്തിന്റെ പേര് നൽകുക.",
        "none": "ഇന്ത്യയിൽ പൊരുത്തപ്പെടുന്ന സ്ഥലം കണ്ടെത്താനായില്ല. അക്ഷരവിന്യാസം മാറ്റിയോ സമീപ നഗരത്തിന്റെ പേര് നൽകിയോ ശ്രമിക്കുക.",
        "search_error": "സ്ഥലങ്ങൾ കണ്ടെത്താനായില്ല. ഇന്റർനെറ്റ് പരിശോധിച്ച് വീണ്ടും ശ്രമിക്കുക.",
        "choose": "നിങ്ങളുടെ സ്ഥലം തിരഞ്ഞെടുക്കുക",
        "no_locations": "സ്ഥലം നൽകി പൊരുത്തമുള്ള സ്ഥലങ്ങൾ കാണാൻ 'സ്ഥലങ്ങൾ കണ്ടെത്തുക' തിരഞ്ഞെടുക്കുക.",
        "forecasting": "കാലാവസ്ഥാ പ്രവചനം ലഭ്യമാക്കുന്നു...",
        "forecast_error": "ഈ സ്ഥലത്തിന്റെ കാലാവസ്ഥാ പ്രവചനം ലഭിച്ചില്ല. വീണ്ടും ശ്രമിക്കുക.",
        "retry": "പ്രവചനം വീണ്ടും നേടുക",
        "forecast_heading": "പ്രവചനത്തിന്റെ സ്ഥലം:",
        "three_day": "മൂന്ന് ദിവസത്തെ പ്രവചനം",
        "date": "തീയതി",
        "min": "കുറഞ്ഞത് °C",
        "max": "കൂടിയത് °C",
        "rain": "മഴ (മില്ലിമീറ്റർ)",
        "assessment": "AI വിളരോഗ സാധ്യതാ വിലയിരുത്തൽ",
        "guidance": "രോഗ മാർഗ്ഗനിർദ്ദേശം വായിക്കുക",
        "no_risk": "ലഭിച്ച വിവരങ്ങളിൽ പ്രത്യേക രോഗസാധ്യത കണ്ടെത്തിയില്ല. അതിനർത്ഥം വിളയ്ക്ക് രോഗമില്ല എന്നല്ല.",
        "disclaimer": "ലഭിച്ച കാർഷിക വിവരങ്ങളെയും കാലാവസ്ഥാ പ്രവചനത്തെയും അടിസ്ഥാനമാക്കിയുള്ള AI പരിശോധനയാണിത്. ഇത് സ്ഥിരീകരിച്ച രോഗനിർണയമോ ഔദ്യോഗിക കാർഷിക മുന്നറിയിപ്പോ അല്ല. പ്രധാന തീരുമാനങ്ങൾക്ക് പ്രാദേശിക കൃഷി വിജ്ഞാന കേന്ദ്രത്തെയോ (KVK) കാർഷിക ഉദ്യോഗസ്ഥനെയോ സമീപിക്കുക.",
        "watch": "ശ്രദ്ധിക്കുക",
        "elevated": "കൂടിയ അപകടസാധ്യത",
        "insufficient": "മതിയായ തെളിവില്ല",
        "example": "ഉദാ. കർണാൽ, ഹരിയാന",
        "crop_example": "ഉദാ. ആപ്പിൾ, ചോളം, അരി, ഗോതമ്പ്",
    },
}


def weather_text(language, key):
    """Return translated UI text, with English fallback for missing keys."""
    language = language.split(" (")[0]
    language_dict = WEATHER_TEXT.get(language, WEATHER_TEXT["English"])
    return language_dict.get(key, WEATHER_TEXT["English"].get(key, key))


def find_locations(place):
    """Find matching places and return their coordinates."""
    response = requests.get(
        GEOCODING_URL,
        params={
            "name": place.strip(),
            "count": 5,
            "language": "en",
            "format": "json",
        },
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    results = response.json().get("results", [])
    return [
        {
            "name": item["name"],
            "admin1": item.get("admin1", ""),
            "country": item.get("country", ""),
            "latitude": item["latitude"],
            "longitude": item["longitude"],
        }
        for item in results
    ]


def get_forecast(latitude, longitude):
    """Retrieve the next three days of weather data."""
    response = requests.get(
        FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m,relative_humidity_2m,precipitation",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "forecast_days": 3,
            "timezone": "auto",
        },
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def evaluate_risk(crop, location, forecast, language="English"):
    """Run the evidence-grounded assessment in the selected language."""
    summary, alerts = assess_weather_risk(
        crop=crop,
        location=location,
        forecast=forecast,
        language=language.split(" (")[0],
    )
    return alerts, forecast.get("daily", {}), summary


def render_weather_alerts(language="English"):
    """Render translated weather alerts while preserving session state."""
    language = language.split(" (")[0]

    st.subheader(weather_text(language, "title"))
    st.caption(weather_text(language, "intro"))

    defaults = {
        "weather_locations": [],
        "weather_forecast_key": None,
        "weather_forecast_data": None,
        "weather_alert_data": None,
        "weather_daily_data": None,
        "weather_error": None,
        "weather_summary": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    place = st.text_input(
        weather_text(language, "place"),
        placeholder=weather_text(language, "example"),
        key="weather_place",
    )
    crop = st.text_input(
        weather_text(language, "crop"),
        value="Tomato",
        placeholder=weather_text(language, "crop_example"),
        key="weather_crop",
    ).strip()

    if st.button(weather_text(language, "find"), key="check_weather"):
        if not place.strip():
            st.warning(weather_text(language, "empty"))
        else:
            try:
                with st.spinner(weather_text(language, "searching")):
                    response = requests.get(
                        GEOCODING_URL,
                        params={
                            "name": place.strip(),
                            "count": 20,
                            "language": "en",
                            "format": "json",
                            "countryCode": "IN",
                        },
                        timeout=TIMEOUT,
                    )
                    response.raise_for_status()
                    results = response.json().get("results", [])

                st.session_state.weather_locations = [
                    {
                        "name": item["name"],
                        "admin1": item.get("admin1", ""),
                        "country": item.get("country", ""),
                        "latitude": item["latitude"],
                        "longitude": item["longitude"],
                    }
                    for item in results
                ]

                st.session_state.weather_forecast_key = None
                st.session_state.weather_forecast_data = None
                st.session_state.weather_alert_data = None
                st.session_state.weather_daily_data = None
                st.session_state.weather_error = None
                st.session_state.weather_summary = None

                if not results:
                    st.warning(weather_text(language, "none"))
            except requests.RequestException:
                st.error(weather_text(language, "search_error"))

    locations = st.session_state.weather_locations
    if not locations:
        st.info(weather_text(language, "no_locations"))
        return

    labels = [
        " — ".join(
            part for part in (item["name"], item["admin1"], item["country"]) if part
        )
        for item in locations
    ]

    selected_label = st.selectbox(
        weather_text(language, "choose"),
        labels,
        key="weather_location_choice",
    )
    selected = locations[labels.index(selected_label)]
    forecast_key = (
        selected["latitude"],
        selected["longitude"],
        crop,
        language,
    )

    if st.session_state.weather_forecast_key != forecast_key:
        try:
            with st.spinner(weather_text(language, "forecasting")):
                forecast = get_forecast(
                    selected["latitude"], selected["longitude"]
                )
                alerts, daily, summary = evaluate_risk(
                    crop=crop,
                    location=selected_label,
                    forecast=forecast,
                    language=language,
                )

            st.session_state.weather_forecast_key = forecast_key
            st.session_state.weather_forecast_data = forecast
            st.session_state.weather_alert_data = alerts
            st.session_state.weather_daily_data = daily
            st.session_state.weather_error = None
            st.session_state.weather_summary = summary
        except Exception as exc:
            print(f"Weather risk assessment failed: {exc}")
            st.session_state.weather_forecast_key = None
            st.session_state.weather_forecast_data = None
            st.session_state.weather_alert_data = None
            st.session_state.weather_daily_data = None
            st.session_state.weather_summary = None
            st.session_state.weather_error = weather_text(language, "forecast_error")

    if st.session_state.weather_error:
        st.error(st.session_state.weather_error)
        if st.button(weather_text(language, "retry"), key="retry_weather"):
            st.session_state.weather_forecast_key = None
            st.session_state.weather_error = None
            st.rerun()
        return

    daily = st.session_state.weather_daily_data
    alerts = st.session_state.weather_alert_data
    if daily is None or alerts is None:
        return

    st.markdown(
        f"**{weather_text(language, 'forecast_heading')}** {selected_label}"
    )

    dates = daily.get("time", [])
    highs = daily.get("temperature_2m_max", [])
    lows = daily.get("temperature_2m_min", [])
    rain_totals = daily.get("precipitation_sum", [])

    if dates:
        st.markdown(f"**{weather_text(language, 'three_day')}**")
        rows = []
        for i in range(len(dates)):
            rows.append(
                {
                    weather_text(language, "date"): dates[i],
                    weather_text(language, "min"): lows[i] if i < len(lows) else None,
                    weather_text(language, "max"): highs[i] if i < len(highs) else None,
                    weather_text(language, "rain"): (
                        rain_totals[i] if i < len(rain_totals) else None
                    ),
                }
            )
        st.dataframe(rows, use_container_width=True, hide_index=True)

    st.markdown(f"**{weather_text(language, 'assessment')}**")
    summary = st.session_state.weather_summary
    if summary:
        st.write(summary)

    level_keys = {
        "Watch": "watch",
        "Elevated": "elevated",
        "Insufficient evidence": "insufficient",
    }
    if alerts:
        for alert in alerts:
            level_key = level_keys.get(alert.get("level", "Watch"), "watch")
            display_level = weather_text(language, level_key)
            st.warning(f"{display_level}: {alert.get('disease', 'Potential crop disease')}")
            if alert.get("description"):
                st.write(alert["description"])
            if alert.get("evidence"):
                st.caption(alert["evidence"])
            source = alert.get("source", "")
            if source.startswith("https://"):
                st.markdown(
                    f"[{weather_text(language, 'guidance')}]({source})"
                )
    else:
        st.info(weather_text(language, "no_risk"))

    st.caption(weather_text(language, "disclaimer"))
