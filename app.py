from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)

# ✅ 从 Railway 环境变量中读取 OpenAI 密钥
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def index():
    return "✅ Voice AI App is running."

@app.route("/voice", methods=["POST"])
def voice():
    # ✅ 尝试从 Twilio 识别结果中提取用户说的话
    user_input = request.form.get("SpeechResult") or request.form.get("Body") or "你好"

    print(f"[User Input]: {user_input}")  # ✅ 打印用户说了什么

    try:
        # ✅ 调用 OpenAI 进行回答
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly AI voice assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=100
        )
        ai_text = response.choices[0].message.content.strip()
        print(f"[OpenAI Reply]: {ai_text}")  # ✅ 打印 AI 返回什么

    except Exception as e:
        print(f"[OpenAI ERROR]: {e}")  # ✅ 打印错误日志
        ai_text = "Sorry, I ran into a problem."

    # ✅ 返回 TwiML 响应
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna" language="en-US">{ai_text}</Say>
</Response>"""
    return Response(twiml, mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway 默认用 PORT 环境变量
    app.run(host="0.0.0.0", port=port)
