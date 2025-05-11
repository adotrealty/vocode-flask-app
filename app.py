from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Simple Twilio Voice App Running"

@app.route("/voice", methods=["POST"])
def voice():
    # 返回语音识别接口
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather input="speech dtmf" timeout="5" language="en-US" action="/ai">
        <Say voice="Polly.Joanna">Hello, how can I help you?</Say>
    </Gather>
    <Say voice="Polly.Joanna">I didn't catch that. Goodbye!</Say>
</Response>"""
    return Response(twiml, mimetype="text/xml")

@app.route("/ai", methods=["POST"])
def ai():
    # 这里只返回静态内容
    user_input = request.form.get("SpeechResult") or "Nothing heard"
    print("User said:", user_input)  # 可在 Railway logs 中看到
    response_twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">You said: {user_input}</Say>
</Response>"""
    return Response(response_twiml, mimetype="text/xml")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
