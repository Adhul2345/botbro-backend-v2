import requests
from config import GROQ_API_KEY

def get_bot_reply(memory, user_msg):
    print("⚡ Sending request to Groq...")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # System prompt to give BotBro that Gen Z + Manglish VIBE 💥
    system_prompt = {
        "role": "system",
        "content": (
            "You are BotBro — a fun, sarcastic, slightly unhinged digital bestie. "
            "You talk like a Gen Z Kerala kid with lots of Manglish (Malayalam-English mix), memes, and chill vibes. "
            "Be casual, funny, helpful, and NEVER too formal. Example: if user says 'hi', you might say 'Yo macha! Enth paripadi?' 😎"
        )
    }

    # Check and log memory
    try:
        history = memory.get_messages()
        if not isinstance(history, list):
            raise ValueError("❌ memory.get_messages() must return a list")

        for msg in history:
            if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
                raise ValueError(f"❌ Invalid message format: {msg}")
    except Exception as err:
        print(f"🧠 Memory error: {err}")
        return "❌ Memory format messed up. Check backend memory logic bro."

    payload = {
        "model": "llama3-70b-8192",  # 🔥 Best performing Groq model rn
        "messages": [system_prompt] + history + [{"role": "user", "content": user_msg}],
        "temperature": 0.85  # more creative & chaotic 🤪
    }

    print("📦 Payload to Groq:")
    print(payload)

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )

        response.raise_for_status()

        reply = response.json()["choices"][0]["message"]["content"]
        print(f"✅ Groq replied: {reply}")
        return reply

    except requests.exceptions.HTTPError as err:
        print(f"🚨 HTTP error from Groq: {err.response.status_code} - {err.response.text}")
        return f"❌ Groq Error {err.response.status_code}: {err.response.text}"

    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return "💀 Bro I had a brain fart... Try again?"
