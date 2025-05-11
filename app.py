from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Voice app is running."

@app.route("/voice", methods=["POST"])
def voice():
    # 语音识别 + fallback + 不挂断
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather input="speech" timeout="5" speechTimeout="auto" language="en-US" action="/process" method="POST">
        <Say voice="Polly.Joanna">Hello, how can I help you today?</Say>
    </Gather>
    <Say voice="Polly.Joanna">Sorry, I didn't hear anything. Goodbye!</Say>
</Response>"""
    return Response(twiml, mimetype="text/xml")

@app.route("/process", methods=["POST"])
def process():
    user_input = request.form.get("SpeechResult", "").strip()
    print(f"User said: {user_input}")

    if not user_input:
        say = "Sorry, I couldn't hear you."
    else:
        say = f"You said: {user_input}"

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">{say}</Say>
    <Redirect>/voice</Redirect>
</Response>"""
    return Response(twiml, mimetype="text/xml")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
