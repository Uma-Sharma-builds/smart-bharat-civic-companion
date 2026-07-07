import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-1.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

SYSTEM_PROMPT = """You are "Smart Bharat Sahayak", an AI-powered civic companion for Indian citizens.
Your job:
1. Help citizens access government services (schemes, documents like Aadhar, PAN, ration card, etc.)
2. Help them report public issues (potholes, garbage, broken streetlights, water leakage) - guide them on where/how to report.
3. Answer questions about government processes in simple, clear steps.
4. Reply in the same language the user writes in (Hindi, Hinglish, or English).
5. Be friendly, clear, and give step-by-step actionable guidance. Keep answers concise (under 150 words) unless asked for detail.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not GEMINI_API_KEY:
        return jsonify({"reply": "Server error: GEMINI_API_KEY not configured."}), 500

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": SYSTEM_PROMPT + "\n\nUser: " + user_message}]}
        ]
    }

    try:
        resp = requests.post(f"{GEMINI_URL}?key={GEMINI_API_KEY}", json=payload, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        reply = result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        reply = f"Sorry, kuch error aa gaya: {str(e)}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
