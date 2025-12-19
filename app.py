from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "arcee-ai/trinity-mini:free",
        "messages": [
            {
                "role": "system",
                "content": "You are a luxury brand chatbot. Tone is premium, confident, and minimal."
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "temperature": 0.7
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    result = response.json()
    reply = result["choices"][0]["message"]["content"]

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
