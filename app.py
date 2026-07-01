"""
Sereni Guided Calm Video coded prototype.

Run in IntelliJ IDEA terminal:
    source .venv/bin/activate
    python app.py

Then open:
    http://127.0.0.1:5000
"""

import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from openai import OpenAI


load_dotenv()

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

SYSTEM_PROMPT = """
You are Sereni, a calm mental-health support companion for university
students. Respond with short, warm, non-clinical support. Encourage gentle
breathing, rest, and campus wellbeing resources. Do not diagnose. If the user
mentions immediate danger or self-harm, advise them to contact emergency
services or a trusted person right away.
"""


@app.route("/")
def index():
    """Serve the high-fidelity mobile prototype."""
    return send_from_directory(".", "index.html")


@app.route("/assets/<path:filename>")
def assets(filename):
    """Serve image assets used by the prototype."""
    return send_from_directory("assets", filename)


@app.route("/api/health")
def health():
    """Simple endpoint for checking whether Flask is running."""
    return jsonify({
        "status": "ok",
        "app": "Sereni Guided Calm Video Prototype",
    })


@app.route("/api/reflection", methods=["POST"])
def reflection():
    """
    Receive a voice transcript or typed reflection from the frontend.

    The OpenAI API call is ready for real integration. If OPENAI_API_KEY is not
    set in .env, the endpoint returns a polished demo response so the prototype
    can still be presented live.
    """
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "No reflection text was received."}), 400

    if not OPENAI_API_KEY or OPENAI_API_KEY == "paste-your-api-key-here":
        return jsonify({
            "reply": (
                "Demo response: I hear that you took a pause. Keep your next "
                "step small: drink water, unclench your shoulders, and return "
                "to one task at a time."
            ),
            "demo_mode": True,
        })

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.responses.create(
            model=OPENAI_MODEL,
            instructions=SYSTEM_PROMPT,
            input=message,
        )
        return jsonify({
            "reply": response.output_text,
            "demo_mode": False,
        })
    except Exception as error:
        return jsonify({
            "error": "OpenAI API request failed.",
            "details": str(error),
        }), 500


@app.route("/api/transcribe", methods=["POST"])
def transcribe_placeholder():
    """
    Placeholder endpoint for future server-side speech-to-text.

    The current prototype uses browser SpeechRecognition for live demo. This
    route is intentionally left ready for OpenAI audio transcription wiring.
    """
    return jsonify({
        "status": "placeholder",
        "message": "Connect this endpoint to OpenAI audio transcription when needed.",
    })


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
