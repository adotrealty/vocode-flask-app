from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "AI Voice Assistant is running."

@app.route("/voice", methods=["POST"])
def voice():
    # 获取用户语音输入
    user_input = request.form.get("SpeechResult") or request.form.get("Body") or ""

    if user_input.strip() == "":
        # 用户没说话，或第一次进入通话
        twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather input="speech" timeout="5" language="en-US">
        <Say>Hello, how can I help you today?</Say>
    </Gather>
    <Say>I didn’t catch that. Let’s try again.</Say>
    <Redirect>/voice</Redirect>
</Response>"""
        return Response(twiml, mimetype="text/xml")

    try:
        # 调用 OpenAI 获取回复
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI voice assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        ai_text = completion["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"OpenAI error: {e}")
        ai_text = "Sorry, I ran into a problem."

    # 构造 TwiML 响应，并继续对话
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{ai_text}</Say>
    <Redirect>/voice</Redirect>
</Response>"""
    return Response(twiml, mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
