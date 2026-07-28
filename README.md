# AI Chatbot for Student Support Service

Ek din me complete karne ke liye step-by-step guide.

## Kaise kaam karta hai (samajhne ke liye)
1. User koi sawal type karta hai (jaise "library timing kya hai?")
2. Pehle app apni khud ki **Knowledge Base** (knowledge_base.py) me check karta hai — agar keyword match ho jaye (jaise "library"), turant fixed answer de deta hai. Ye FREE hai, koi API call nahi lagti.
3. Agar knowledge base me match nahi mila, to app **AI (OpenRouter API)** ko sawal bhejta hai aur uska jawab dikhata hai. Ye general/open-ended sawalon ke liye hai.

## Project Structure
```
student_support_chatbot/
├── app.py                  # Main Flask backend
├── knowledge_base.py       # Fixed FAQ answers
├── requirements.txt        # Libraries needed
├── .env                    # Your API key (aapko banani hai)
└── templates/
    └── index.html          # Chat UI (website)
```

## Step-by-step instructions

Neeche chat me detailed guide di gayi hai. Short summary:

1. Python aur VS Code install karo
2. Ye saari files ek folder me daalo
3. OpenRouter.ai par free account banao, API key lo
4. `.env` file banao us key ke saath
5. `pip install -r requirements.txt`
6. `python app.py`
7. Browser me `http://127.0.0.1:5000` kholo

## Presentation/Viva ke liye points
- **Problem Statement**: College students ko common queries (fees, library, hostel, etc.) ke liye baar baar office jana padta hai — chatbot se instant answers milte hain.
- **Approach**: Hybrid system — rule-based Knowledge Base (fast, accurate for known FAQs) + AI/LLM (OpenRouter API) for open-ended questions
- **Tech Stack**: Python, Flask (backend), HTML/CSS/JS (frontend), OpenRouter API (AI)
- **Future Scope**: Database integration for dynamic FAQs, login system, multilingual support, voice input
