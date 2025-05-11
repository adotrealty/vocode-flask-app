from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Twilio Voice App is running."

# 第一次接听电话：说 hello 并收集语音，超时后转 /ai
@app.route("/voice", methods=["POST"])
def voice():
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Gather input="speech" timeout="5" language="en-US" action="/ai">
    <Say voice="Polly.Joanna">Hello, how can I help you?</Say>
  </Gather>
  <Say voice="Polly.Joanna">I didn't hear anything. Goodbye!</Say>
</Response>"""
    return Response(twiml, mimetype="text/xml")

# 接收语音识别后的文本，简单回应
@app.route("/ai", methods=["POST"])
def ai():
    user_input = request.form.get("SpeechResult") or "(No speech detected)"
    print(f"User said: {user_input}")

    # 简单的固定回应逻辑
    if "name" in user_input.lower():
        response_text = "My name is Joanna, your AI assistant."
    elif "weather" in user_input.lower():
        response_text = "I'm sorry, I don't have weather data right now."
    else:
        response_text = "I heard you say: " + user_input

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="Polly.Joanna">{response_text}</Say>
</Response>"""
    return Response(twiml, mimetype="text/xml")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
