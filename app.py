from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)

# 获取 OpenAI 的 API Key
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Twilio AI Voice Assistant is running."

@app.route("/voice", methods=["POST"])
def voice():
    # Step 1: 如果还没有用户输入，则先欢迎并收集语音
    speech_result = request.form.get("SpeechResult")
    if not speech_result:
        gather_twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">Hello, how can I help you today?</Say>
    <Gather input="speech" timeout="5" speechTimeout="auto" action="/voice" method="POST">
        <Say voice="Polly.Joanna">Please say something after the beep.</Say>
    </Gather>
</Response>"""
        return Response(gather_twiml, mimetype="text/xml")

    # Step 2: 用户说完后，将其内容发送给 ChatGPT
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly voice assistant."},
                {"role": "user", "content": speech_result}
            ]
        )
        reply = completion["choices"][0]["message"]["content"]
    except Exception as e:
        print("OpenAI error:", e)
        reply = "Sorry, something went wrong when processing your request."

    # Step 3: 返回 AI 回复
    response_twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">{reply}</Say>
</Response>"""
    return Response(response_twiml, mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
