# AI English Tutor

AI English Tutor ek intelligent FastAPI application hai jo `LangChain`, `Groq LLM`, aur `edge-tts` ka use karke users ki English communication skills improve karne mein madad karta hai.

## 🚀 Features
- **Interactive Chat:** AI-powered tutor jo real-time feedback deta hai.
- **Voice Support:** Text-to-Speech (edge-tts) ka use karke tutor ki awaaz sun sakte hain.
- **History Tracking:** SQLite database ka use karke conversation history save karta hai.
- **Deployment Ready:** Render par deployment ke liye optimized.

## 🛠 Tech Stack
- **Backend:** FastAPI
- **LLM:** Groq (Llama-3)
- **Framework:** LangChain
- **TTS:** edge-tts
- **Database:** SQLite

## 📂 Project Structure
```text
├── app/
│   ├── app.py              # Main FastAPI application
│   ├── services/
│   │   └── ai_tutor_service.py # AI & Audio Logic
│   └── prompts/
│       └── ai_tutor_prompt.py  # Prompt Engineering
├── requirements.txt
├── .gitignore
└── README.md