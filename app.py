from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)

# 读取 OpenAI 密钥
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "AI Voice Assistant is running."

@app.route("/voice", methods=["POST"])
def voice():
    # 初次进入语音系统，播放欢迎词并等待说话
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
    print(f"[User said]: {user_input}")

    if not user_input:
        ai_text = "Sorry, I couldn't hear you."
    else:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful and friendly voice assistant."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=100,
                temperature=0.7,
                timeout=10
            )
            ai_text = completion.choices[0].message.content.strip()
            print(f"[AI replied]: {ai_text}")
        except Exception as e:
            print(f"[OpenAI ERROR]: {e}")
            ai_text = "Sorry, I ran into a problem."

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">{ai_text}</Say>
    <Redirect>/voice</Redirect>
</Response>"""
    return Response(twiml, mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
