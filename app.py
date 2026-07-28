# app.py
# -----------------------------------------------------------
# SMART STUDENT SUPPORT AI CHATBOT - Main Backend
# Features: FAQ + Mood Detection + Crisis Helpline
#           + Chat History (SQLite) + Admin Dashboard
# -----------------------------------------------------------

import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import requests

# hamari khud ki file se functions import kar rahe hain
from knowledge_base import (
    get_faq_answer, detect_mood, MOOD_REPLY,
    is_crisis, CRISIS_MESSAGE, detect_language
)

load_dotenv()  # .env file se API key load karo

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DB_NAME = "chat_history.db"


# ============ DATABASE SETUP ============
def init_db():
    """Pehli baar chalne par database aur table bana do."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            user_message TEXT,
            bot_reply TEXT,
            topic TEXT,
            mood TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_chat(user_message, bot_reply, topic, mood):
    """Har baat-cheet ko database me save karo (analytics ke liye)."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO chats (time, user_message, bot_reply, topic, mood) VALUES (?, ?, ?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
         user_message, bot_reply, topic or "general", mood or "neutral")
    )
    conn.commit()
    conn.close()


# ============ AI REPLY (OpenRouter) ============
def get_ai_reply(message, lang="en"):
    """Jab FAQ me answer na mile to AI se jawab lo."""
    try:
        language_instruction = (
            "The student wrote in Hindi/Hinglish, so reply in Hindi (Hinglish, Roman script)."
            if lang == "hi" else
            "Reply in English by default. Only switch to Hindi if the student explicitly writes in Hindi."
        )
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": (
                        "You are a friendly Student Support Assistant for a college. "
                        "Help students with studies, career, and general problems. "
                        "Keep replies short, simple, and caring. "
                        + language_instruction
                    )},
                    {"role": "user", "content": message},
                ],
            },
            timeout=30,
        )
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print("AI Error:", e)
        return "Maaf kijiye, abhi main jawab nahi de pa raha. Thodi der baad try karo. 🙏"


# ============ ROUTES ============
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"reply": "Kuch to likho 🙂"})

    # ---- STEP 0: Language detect karo (default English, Hindi/Hinglish par switch) ----
    lang = detect_language(user_message)

    # ---- STEP 1: Crisis check (sabse pehle, safety ke liye) ----
    if is_crisis(user_message):
        crisis_reply = CRISIS_MESSAGE[lang]
        save_chat(user_message, crisis_reply, "crisis", "crisis")
        return jsonify({"reply": crisis_reply, "mood": "crisis"})

    # ---- STEP 2: Mood detect karo ----
    mood = detect_mood(user_message)
    mood_prefix = MOOD_REPLY.get(mood, {}).get(lang, "") if mood else ""

    # ---- STEP 3: FAQ me answer dhoondo ----
    faq_answer, topic = get_faq_answer(user_message, lang)

    if faq_answer:
        reply = mood_prefix + faq_answer
    else:
        # ---- STEP 4: FAQ me nahi mila to AI se poocho ----
        ai_answer = get_ai_reply(user_message, lang)
        reply = mood_prefix + ai_answer
        topic = "general"

    # ---- STEP 5: Database me save karo ----
    save_chat(user_message, reply, topic, mood)

    return jsonify({"reply": reply, "mood": mood or "neutral"})


@app.route("/dashboard")
def dashboard():
    """Admin dashboard - analytics dikhata hai."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Total chats
    c.execute("SELECT COUNT(*) FROM chats")
    total = c.fetchone()[0]

    # Topic wise count (kaunsa topic sabse zyada pucha gaya)
    c.execute("SELECT topic, COUNT(*) FROM chats GROUP BY topic ORDER BY COUNT(*) DESC")
    topics = c.fetchall()

    # Mood wise count
    c.execute("SELECT mood, COUNT(*) FROM chats GROUP BY mood ORDER BY COUNT(*) DESC")
    moods = c.fetchall()

    # Last 10 chats
    c.execute("SELECT time, user_message, mood FROM chats ORDER BY id DESC LIMIT 10")
    recent = c.fetchall()

    conn.close()

    return render_template("dashboard.html",
                           total=total, topics=topics,
                           moods=moods, recent=recent)


if __name__ == "__main__":
    init_db()  # database ready karo
    app.run(debug=True)