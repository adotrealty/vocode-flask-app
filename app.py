from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna" language="en-US">Hello, this is your AI assistant. I received your request.</Say>
</Response>"""
    return Response(twiml, mimetype="text/xml")

@app.route("/", methods=["GET"])
def home():
    return "AI Voice app is running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
