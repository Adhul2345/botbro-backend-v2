print("🔥 Starting BotBro server...")
from flask import Flask, request, jsonify
print("✔ Flask imported")

from flask_cors import CORS
print("✔ CORS imported")

from memory.chat_memory import ChatMemory
print("✔ ChatMemory imported")

from llm.groq_llm import get_bot_reply
print("✔ get_bot_reply imported")

import os

# Initialize app
app = Flask(__name__)
CORS(app)  # Allow cross-origin (Flutter can connect)

# Load memory
memory = ChatMemory(memory_file='data/memory.json')


@app.route("/")
def home():
    return "🤖 BotBro is Alive!"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message")

    if not user_msg:
        return jsonify({"error": "No message provided"}), 400

    # Add user message to memory
    memory.add_message("user", user_msg)

    # Get bot reply
    bot_reply = get_bot_reply(memory, user_msg)

    # Add bot reply to memory
    memory.add_message("bot", bot_reply)

    return jsonify({"reply": bot_reply})


@app.route("/clear_memory", methods=["POST"])
def clear_memory():
    memory.clear_memory()
    return jsonify({"message": "Memory cleared!"})


@app.route("/get_memory", methods=["GET"])
def get_memory():
    return jsonify(memory.get_memory())


if __name__ == "__main__":
    print("running flask server")
    app.run(host="0.0.0.0", port=5000, debug=True)
