from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)

# ✅ 读取 OpenAI 密钥（确保在 Railway 中配置 OPENAI_API_KEY）
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "AI Voice Assistant is running."

@app.route("/voice", methods=["POST"])
def voice():
    user_input = request.form.get("SpeechResult") or ""

    # 第一次没说话 → 欢迎语 + 进入语音等待
    if user_input.strip() == "":
        twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather input="speech" timeout="5" speechTimeout="auto" language="en-US" action="/voice" method="POST">
        <Say voice="Polly.Joanna">Hello, how can I help you today?</Say>
    </Gather>
    <Say>I didn’t hear anything. Goodbye!</Say>
</Response>"""
        return Response(twiml, mimetype="text/xml")

    print(f"[User]: {user_input}")  # ✅ 打印用户说了什么

    try:
        # ✅ 调用 GPT（回复尽量短，控制超时风险）
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a concise and friendly AI voice assistant. Reply in short and clear sentences."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=80,
            temperature=0.7
        )
        ai_text = completion["choices"][0]["message"]["content"].strip()
        print(f"[AI]: {ai_text}")  # ✅ 打印 AI 回复
    except Exception as e:
        print(f"[OpenAI error]: {e}")  # ✅ 打印错误日志
        ai_text = "Sorry, I ran into a problem."

    # ✅ 说完后继续进入下一轮等待，不挂断
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">{ai_text}</Say>
    <Redirect>/voice</Redirect>
</Response>"""
    return Response(twiml, mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
