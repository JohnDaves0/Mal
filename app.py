@app.route("/")
def home():
    return "ElevenLabs TTS Flask is running!"


import requests
from flask import Flask, request, jsonify, send_file
from io import BytesIO

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This allows all origins by default

import os

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
VOICE_ID = os.environ.get("VOICE_ID")


@app.route("/api/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Missing text"}), 400

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.85
        }
    }

    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        json=payload,
        headers=headers
    )

    if response.status_code != 200:
        return jsonify({"error": "TTS request failed", "details": response.text}), 500

    return send_file(BytesIO(response.content), mimetype="audio/mpeg")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if not set
    app.run(host="0.0.0.0", port=port)

