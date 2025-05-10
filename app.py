from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")  # 确保在 Railway 设置过环境变量

@app.route("/", methods=["GET"])
def home():
    return "AI Voice App is running."

@app.route("/voice", methods=["POST"])
def voice():
    user_input = request.form.get("SpeechResult") or request.form.get("Body") or "你好"

    try:
        chat_reply = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个温和的中文语音助手"},
                {"role": "user", "content": user_input}
            ]
        )
        ai_text = chat_reply["choices"][0]["message"]["content"][:300]  # 截断300字符，防止Twilio播放中断
        print(f"✅ AI回应：{ai_text}")
    except Exception as e:
        print(f"❌ OpenAI错误: {e}")
        ai_text = "很抱歉，我刚才好像出错了。"

    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="zh-CN" voice="Alice">{ai_text}</Say>
</Response>"""
    return Response(twiml_response, mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
