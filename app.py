from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Vocode Flask App is Running!"

@app.route("/voice", methods=["POST"])
def voice():
    print("📞 Incoming call from Twilio")
    twiml_response = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Hello! This is your Railway app speaking. It works!</Say>
</Response>"""
    return Response(twiml_response, mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
