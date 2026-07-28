# knowledge_base.py
# -----------------------------------------------------------
# Ab har FAQ answer ke DO versions hain: English aur Hindi
# Bot detect karega student kis bhasha me baat kar raha hai
# -----------------------------------------------------------

# ============ 1. COLLEGE FAQ (English + Hindi dono) ============
FAQ = {
    "library": {
        "en": "📚 Library timings: Monday to Saturday, 9:00 AM to 6:00 PM. Closed on Sunday.",
        "hi": "📚 Library timings: Somwar se Shanivar, subah 9:00 AM se shaam 6:00 PM tak. Sunday band rehti hai."
    },
    "fees": {
        "en": "💰 To pay fees, go to the 'Fee Payment' section on the college website. The last date is posted on the notice board at the start of each semester.",
        "hi": "💰 Fees jama karne ke liye college website ke 'Fee Payment' section me jao. Last date har semester ke start me notice board par lagti hai."
    },
    "hostel": {
        "en": "🏠 For hostel, submit your application at the Hostel Office (Block C). Warden meeting time: 10 AM - 4 PM.",
        "hi": "🏠 Hostel ke liye Hostel Office (Block C) me application do. Warden se milne ka time 10 AM - 4 PM hai."
    },
    "exam": {
        "en": "📝 The exam timetable is released on the notice board and website 15 days before exams. Download your hall ticket from the portal.",
        "hi": "📝 Exam timetable exam se 15 din pehle notice board aur website par aata hai. Hall ticket portal se download karo."
    },
    "attendance": {
        "en": "📊 Minimum 75% attendance is required to sit for exams. Check your attendance on the student portal.",
        "hi": "📊 Exam me baithne ke liye minimum 75% attendance zaroori hai. Apni attendance student portal par check karo."
    },
    "scholarship": {
        "en": "🎓 For scholarships, submit your documents at the Accounts Office. For government scholarships, use the NSP portal.",
        "hi": "🎓 Scholarship ke liye Accounts Office me documents jama karo. Government scholarship ke liye NSP portal use karo."
    },
    "placement": {
        "en": "💼 The placement cell is in Block A. You must register before campus drives.",
        "hi": "💼 Placement cell Block A me hai. Campus drives se pehle registration karwana zaroori hai."
    },
    "timetable": {
        "en": "🗓️ You can find the class timetable on your department notice board or the student portal.",
        "hi": "🗓️ Class timetable apne department notice board ya student portal par milega."
    },
    "wifi": {
        "en": "📶 Get the campus WiFi password from the IT department (Block B). Your college ID is required.",
        "hi": "📶 Campus WiFi ka password IT department (Block B) se lo. Apni college ID zaroori hai."
    },
    "canteen": {
        "en": "🍔 The canteen is open from 8 AM to 7 PM.",
        "hi": "🍔 Canteen subah 8 AM se shaam 7 PM tak khuli rehti hai."
    },
}

# Keywords (English + Hindi dono, taaki dono language me match ho)
FAQ_KEYWORDS = {
    "library": ["library", "book", "kitab", "padhai room"],
    "fees": ["fee", "fees", "payment", "paisa", "shulk"],
    "hostel": ["hostel", "room", "rehna", "warden"],
    "exam": ["exam", "test", "paper", "pariksha", "hall ticket"],
    "attendance": ["attendance", "haziri", "75", "present"],
    "scholarship": ["scholarship", "wazifa", "nsp", "financial help"],
    "placement": ["placement", "job", "naukri", "company", "campus drive"],
    "timetable": ["timetable", "schedule", "class time", "period"],
    "wifi": ["wifi", "wi-fi", "internet", "password net"],
    "canteen": ["canteen", "food", "khana", "mess"],
}


# ============ LANGUAGE DETECTION (naya function) ============
# Common Hindi/Hinglish words jo bataate hain ki student Hindi me baat kar raha hai
HINDI_HINTS = [
    "kya", "hai", "kaise", "kaha", "kahan", "kab", "kyu", "kyun", "kitna",
    "batao", "chahiye", "mujhe", "karo", "ke", "ki", "ka", "mein",
    "hoon", "nahi", "acha", "achha", "theek", "thik", "aap", "tum", "namaste",
    "jankari", "madad", "bata", "kaisa", "kaisi"
]
# Note: words that are ALSO common English words (e.g. "me", "kar", "hi") are
# deliberately excluded from this list to avoid false-positive Hindi detection
# on plain English sentences like "tell me about hostel".


def detect_language(message):
    """
    Detect karo student English me likh raha hai ya Hindi/Hinglish me.
    Return 'hi' (Hindi) ya 'en' (English).
    """
    msg = message.lower()

    # Agar Devanagari (असली हिंदी अक्षर) hain to pakka Hindi
    for ch in msg:
        if '\u0900' <= ch <= '\u097F':
            return "hi"

    # Hinglish words check karo
    words = msg.split()
    for w in words:
        # word ko clean karke check karo
        clean = w.strip("?.,!")
        if clean in HINDI_HINTS:
            return "hi"

    # Warna English maan lo
    return "en"


import re


def get_faq_answer(message, lang="en"):
    """Message me FAQ keyword dhoondo aur di gayi language me answer do."""
    msg = message.lower()
    for topic, keywords in FAQ_KEYWORDS.items():
        for word in keywords:
            # Multi-word keywords (e.g. "campus drive") -> plain substring check.
            # Single-word keywords -> whole-word match so "fee" doesn't match
            # inside "feeling", "test" doesn't match inside "testimony", etc.
            if " " in word:
                if word in msg:
                    return FAQ[topic][lang], topic
            else:
                if re.search(r"\b" + re.escape(word) + r"\b", msg):
                    return FAQ[topic][lang], topic
    return None, None


# ============ 2. MOOD / EMOTION DETECTION (English + Hindi replies) ============
MOOD_WORDS = {
    "sad": ["sad", "udaas", "dukhi", "cry", "rona", "akela", "lonely", "unhappy", "depress"],
    "stressed": ["stress", "tension", "pressure", "anxious", "ghabra", "worried", "pareshan", "dar", "fail", "overwhelm"],
    "happy": ["happy", "khush", "great", "awesome", "thanks", "thank you", "shukriya", "good", "achha"],
    "angry": ["angry", "gussa", "frustrated", "irritate", "hate"],
}

# Mood replies ab dono language me
MOOD_REPLY = {
    "sad": {
        "en": "😔 It seems you're feeling a bit low. That's okay — I'm here to help you. ",
        "hi": "😔 Lagta hai aap thoda low feel kar rahe ho. Koi baat nahi, main yahan hoon aapki help ke liye. "
    },
    "stressed": {
        "en": "😌 Feeling a little stressed? Take a deep breath — everything will be fine. Let me help you. ",
        "hi": "😌 Thodi tension lag rahi hai? Deep breath lo — sab theek ho jayega. Main aapki madad karta hoon. "
    },
    "happy": {
        "en": "😊 Great to see you happy! ",
        "hi": "😊 Aapko khush dekhkar accha laga! "
    },
    "angry": {
        "en": "😟 It seems you're upset. Let me try to understand and help. ",
        "hi": "😟 Lagta hai aap upset ho. Main samajhne ki koshish karta hoon. "
    },
}


def detect_mood(message):
    """Message ka mood pata karo. Koi mood nahi mila to None."""
    msg = message.lower()
    for mood, words in MOOD_WORDS.items():
        for word in words:
            if word in msg:
                return mood
    return None


# ============ 3. CRISIS DETECTION (English + Hindi message) ============
CRISIS_WORDS = [
    "suicide", "kill myself", "end my life", "marna chahta", "marna chahti",
    "give up", "no reason to live", "self harm", "hurt myself", "khudkushi",
    "jeena nahi", "zindagi khatam", "can't go on", "hopeless"
]

CRISIS_MESSAGE = {
    "en": (
        "❤️ I can understand you're going through a very tough time, and your feelings are completely valid. "
        "You are not alone — there are people who want to listen right now:\n\n"
        "📞 <b>Tele-MANAS (Govt. of India):</b> 14416 or 1-800-891-4416 (24x7, free)\n"
        "📞 <b>KIRAN Mental Health Helpline:</b> 1800-599-0019 (24x7, free)\n\n"
        "Please call one of these numbers now, or talk to someone you trust (parent, teacher, friend). "
        "You matter, and help is available. 🙏"
    ),
    "hi": (
        "❤️ Main samajh sakta hoon ki aap bahut mushkil waqt se guzar rahe ho, aur aapki feelings bilkul valid hain. "
        "Aap akele nahi ho — kuch log hain jo abhi aapki baat sunna chahte hain:\n\n"
        "📞 <b>Tele-MANAS (Govt. of India):</b> 14416 ya 1-800-891-4416 (24x7, free)\n"
        "📞 <b>KIRAN Mental Health Helpline:</b> 1800-599-0019 (24x7, free)\n\n"
        "Please abhi in me se kisi ek number par call karo, ya kisi bharose wale insaan (parent, teacher, friend) se baat karo. "
        "Aap important ho, aur aapki help ki jayegi. 🙏"
    )
}


def is_crisis(message):
    """Check karo ki message me koi crisis word to nahi."""
    msg = message.lower()
    for word in CRISIS_WORDS:
        if word in msg:
            return True
    return False