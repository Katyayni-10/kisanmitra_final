# 🌾 KisanMitra — Multilingual AI Assistant for Farmers

**KisanMitra (किसान मित्र)** is a voice-first, multilingual AI assistant designed to make agricultural guidance and essential information more accessible to farmers, rural families, and elderly users. Built with Python and Streamlit, it combines crop disease classification, conversational AI, speech processing, crop-health tracking, and experimental weather-based disease-risk screening in one application.

The goal is to make useful information easier to access, especially for users who prefer speaking in their own language rather than typing.

## ✨ Features

### 🌿 1. AI-Powered Crop Disease Detection
- Upload a crop-leaf image for disease classification.
- Uses **EfficientNet-B0**, trained using the **PlantVillage dataset**.
- Provides a predicted disease class to support further agricultural questions.
- Helps users begin investigating possible crop-health issues through an accessible interface.

### 🎙️ 2. Multilingual Voice Assistant
Supports 10 languages:

- English
- Hindi (हिन्दी)
- Punjabi (ਪੰਜਾਬੀ)
- Marathi (मराठी)
- Gujarati (ગુજરાતી)
- Bengali (বাংলা)
- Tamil (தமிழ்)
- Telugu (తెలుగు)
- Kannada (ಕನ್ನಡ)
- Malayalam (മലയാളം)

The voice workflow integrates:
- **Whisper** for speech-to-text.
- **Groq-hosted language models** for AI-generated responses.
- **gTTS (Google Text-to-Speech)** for spoken responses.

Users can interact with the assistant to ask agricultural questions and access general informational guidance.

### 🌱 3. Crop Health Journal
- Record crop-health observations.
- Maintain a history of crop-related entries.
- Review observations over time to support crop monitoring.
- Make crop tracking more accessible through the application's multilingual workflow.

### 🌦️ 4. Weather-Based Crop Disease Risk Screening
- Select a location and crop.
- Retrieve weather forecasts through **Open-Meteo**.
- Retrieve relevant agricultural information to ground the assessment.
- Use a Groq-powered workflow to generate a cautious, evidence-oriented risk assessment.
- Display potential risk levels, supporting explanations, and source information where available.

**Important:** This feature is experimental. It is not a validated disease-prediction system and does not replace official agricultural warnings or expert diagnosis.

### 🏛️ 5. Government Scheme Information
Provides conversational guidance about agricultural schemes, including:
- PM-KISAN
- Pradhan Mantri Fasal Bima Yojana (PMFBY)

The assistant can help users understand scheme information and possible application steps. Current eligibility, documentation, and deadlines should always be verified through official government sources.

### 🛡️ 6. General Information and Safety Guidance
- Answer everyday questions through conversational AI.
- Help users understand suspicious claims and potential scams.
- Present information in an accessible, voice-friendly format.
- Include safety guidance and relevant helplines where configured in the application.

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive user interface |
| PyTorch / EfficientNet-B0 | Crop-leaf image classification |
| PlantVillage | Crop disease training dataset |
| Groq API | Conversational AI and risk-assessment generation |
| Whisper | Speech recognition |
| gTTS | Text-to-speech |
| Open-Meteo | Weather forecasts and location lookup |
| DuckDuckGo search integration | Retrieval of relevant information |
| JSON / local files | Local crop-journal data and related application storage |

## 🏗️ Application Workflow

1. **User input:** The user asks a question by voice or text, or uploads a crop-leaf image.
2. **Speech processing:** Voice input is transcribed into text using Whisper.
3. **Crop image analysis:** EfficientNet-B0 classifies the uploaded leaf image.
4. **AI response generation:** The language model generates a response based on the user's query and available context.
5. **Spoken output:** gTTS converts supported responses into speech.
6. **Crop tracking:** The Crop Health Journal allows users to maintain crop observations.
7. **Weather screening:** The application retrieves forecast information and relevant agricultural sources before generating an experimental risk assessment.

## 📁 Project Structure

```text
kisanmitra/
│
├── app.py                 # Main Streamlit application and interface
├── assistant.py           # Conversational AI integration
├── vision.py              # Crop disease image classification
├── voice.py               # Language configuration and voice processing
├── knowledge.py           # Agricultural knowledge, schemes, and safety information
├── crop_journal.py        # Crop Health Journal functionality
├── weather_alerts.py      # Weather-based risk screening interface
├── agri_risk.py           # Retrieval-grounded agricultural risk assessment
├── requirements.txt       # Python dependencies
├── .env                   # Local environment variables (not committed)
└── README.md
```

*Note: Model files, datasets, generated files, and other directories may vary depending on the local setup and Git configuration.*

## 🚀 Getting Started

### Prerequisites

- Python installed and compatible with the project's dependencies.
- Git.
- A Groq API key for features that use Groq.
- Internet connectivity for external AI, weather, search, and speech services as applicable.

### 1. Clone the repository

```bash
git clone https://github.com/Katyayni-10/kisanmitra.git
cd kisanmitra
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If installation fails, check the Python version and the compatibility requirements of the machine-learning and speech-processing libraries.

### 4. Configure environment variables

Create a `.env` file in the project root if required by the current application configuration.

```env
GROQ_API_KEY=your_groq_api_key_here
```

Use the exact environment-variable names expected by the code in `assistant.py` and `agri_risk.py`. Add any other required keys only if the corresponding integrations need them.

**Security:** Never commit API keys, passwords, or other secrets to GitHub.

### 5. Run KisanMitra

```bash
streamlit run app.py
```

Open the local URL printed in the terminal. Streamlit commonly uses:

```text
http://localhost:8501
```

## 🌐 Language Support

| Language | Supported option |
|---|---|
| English | English |
| Hindi | हिन्दी |
| Punjabi | ਪੰਜਾਬੀ |
| Marathi | मराठी |
| Gujarati | ગુજરાતી |
| Bengali | বাংলা |
| Tamil | தமிழ் |
| Telugu | తెలుగు |
| Kannada | ಕನ್ನಡ |
| Malayalam | മലയാളം |

Language availability can vary by feature and by the underlying speech or AI service. Verify that the selected language is applied correctly to the interface, generated assessment, and audio output in the version you run.

## 🌦️ Weather Risk Assessment: Responsible Use

Weather-based risk screening uses forecast conditions and retrieved agricultural information to identify conditions that may be relevant to crop disease. Its output should be interpreted as an initial screening aid, not a confirmed diagnosis.

- Weather conditions alone cannot establish that a disease is present.
- Forecasts and retrieved sources may be incomplete or unavailable.
- AI-generated assessments can be inaccurate.
- Risk levels should not be treated as official agricultural advisories.
- Confirm disease symptoms and treatment choices with a qualified agricultural expert or Krishi Vigyan Kendra (KVK).

## ⚠️ Limitations

- **Image classification:** Predictions are limited by the model's training classes and may not generalize to all real-world field conditions.
- **AI-generated content:** Responses may contain incorrect, outdated, or incomplete information.
- **Weather screening:** The risk-assessment workflow is experimental and requires further validation against trusted agricultural guidance and field observations.
- **Government schemes:** Scheme rules, eligibility criteria, and deadlines can change.
- **External services:** AI, search, weather, and speech features may be affected by connectivity, API availability, quotas, or service limitations.
- **Local storage:** Crop journal entries and related files may be stored locally, depending on the implementation and configuration.

## 🔭 Future Improvements

- Validate crop-risk assessments against agricultural research and field observations.
- Expand disease-class coverage and evaluate classification performance on real-world leaf images.
- Improve consistency of translations across the interface and AI-generated content.
- Add more verified, region-specific agricultural resources.
- Improve error handling and resilience when external services are unavailable.
- Introduce automated tests for core workflows and risk-assessment behavior.
- Improve accessibility for users with limited digital literacy or connectivity.

## 🎯 Project Objectives

KisanMitra brings together several practical AI and software engineering concepts:

- Deep-learning-based image classification.
- Generative AI integration.
- Retrieval-grounded information workflows.
- Speech recognition and text-to-speech.
- Multilingual and accessibility-focused interface design.
- Weather API integration.
- Crop-health tracking and local data management.

## 📄 Disclaimer

KisanMitra is an educational project and is not affiliated with or endorsed by any government agency. Its outputs are for informational purposes only and may be inaccurate. The application does not replace qualified agricultural, medical, or other professional advice. Verify important decisions with appropriate experts and official sources.

---

**Built with 🌱 to make digital assistance more accessible to farming communities.**
