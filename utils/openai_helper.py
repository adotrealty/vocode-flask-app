from flask import Flask, request, Response
import os
from utils.openai_helper import ask_openai

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "AI Voice App is running."

@app.route("/voice", methods=["POST"])
def voice():
    user_input = request.form.get("SpeechResult") or request.form.get("Body") or "你好"

    ai_text = ask_openai(user_input)

    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="en-US" voice="Polly.Joanna">{ai_text}</Say>
</Response>"""

    return Response(twiml_response, mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
