"""
Arabic Voice Chatbot - Flask backend
Browser handles mic input + speech output (Web Speech API).
This Python server just talks to Cohere.

Run: python app.py
Then open: http://127.0.0.1:5000/
"""

import os
import time
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import cohere

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise ValueError("No COHERE_API_KEY found. Create a .env file with COHERE_API_KEY=your_key")

co = cohere.ClientV2(COHERE_API_KEY)

app = Flask(__name__)

SYSTEM_PROMPT = "أنت مساعد ذكي تتحدث باللغة العربية الفصحى وتجيب بإيجاز ووضوح."

# Simple in-memory chat history (resets when server restarts)
chat_history = []


@app.route("/")
def index():
    return render_template("index.html")


def call_cohere_with_retries(messages, max_retries=4):
    """
    Some antivirus/firewall software (McAfee etc.) intermittently resets
    outbound HTTPS connections. Retry a few times with a short pause
    before giving up, so a one-off reset doesn't break the conversation.
    """
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            response = co.chat(
                model="command-a-03-2025",
                messages=messages,
            )

            if not response.message.content or len(response.message.content) == 0:
                print(f"[WARNING] Empty content in response: {response}")
                raise ValueError("Model returned empty content")

            reply_text = response.message.content[0].text

            if "<PAD>" in reply_text:
                print(f"[WARNING] PAD garbage in response, retrying: {response}")
                raise ValueError("Model returned PAD tokens")

            return reply_text

        except Exception as e:
            last_error = e
            print(f"[RETRY {attempt}/{max_retries}] Cohere call failed: {e}")
            if attempt < max_retries:
                time.sleep(1.5 * attempt)  # backs off: 1.5s, 3s, 4.5s...
    raise last_error


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_text = (data or {}).get("text", "").strip()

    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    try:
        chat_history.append({"role": "user", "content": user_text})

        reply = call_cohere_with_retries(
            [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history
        )

        chat_history.append({"role": "assistant", "content": reply})

        return jsonify({"reply": reply})

    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"error": "تعذر الاتصال بالخادم بعد عدة محاولات. حاول مرة أخرى."}), 500


@app.route("/reset", methods=["POST"])
def reset():
    chat_history.clear()
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
