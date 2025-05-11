from flask import Flask, request, Response
from utils.openai_helper import ask_openai

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Voice Assistant Running"

@app.route("/voice", methods=["POST"])
def voice():
    user_input = request.values.get("SpeechResult", "").strip()

    if not user_input:
        # Twilio 听不清或无语音输入
        response = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">I didn’t catch that. Please say that again.</Say>
    <Redirect>/voice</Redirect>
</Response>"""
        return Response(response, mimetype="text/xml")

    ai_response = ask_openai(user_input)

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">{ai_response}</Say>
    <Pause length="1" />
    <Redirect>/voice</Redirect>
</Response>"""
    return Response(twiml, mimetype="text/xml")

if __name__ == "__main__":
    app.run(debug=True)
