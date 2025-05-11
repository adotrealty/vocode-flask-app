from flask import Flask, request, Response
import os
from utils.openai_helper import ask_openai

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "AI Voice Assistant is running."

@app.route("/voice", methods=["POST"])
def voice():
    user_input = request.form.get("SpeechResult") or request.form.get("Body") or "Hello"
    ai_text = ask_openai(user_input)

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna" language="en-US">{ai_text}</Say>
</Response>"""
    return Response(twiml, mimetype="text/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
