from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/voice", methods=["POST"])
def voice():
    user_input = request.form.get("SpeechResult")

    if not user_input:
        # 开场引导用户说话
        twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Gather input="speech" timeout="3" language="en-US">
    <Say>Hello, how can I help you?</Say>
  </Gather>
  <Say>I didn’t hear anything. Goodbye!</Say>
</Response>"""
        return Response(twiml, mimetype="text/xml")

    # 有用户输入后处理
    try:
        print("🎤 User said:", user_input)

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a polite, concise AI voice assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        full_reply = completion["choices"][0]["message"]["content"]
        short_reply = full_reply.strip().split(".")[0] + "."  # 保留第一句话，强制结束于句号
        print("🤖 AI reply:", short_reply)
    except Exception as e:
        print("OpenAI error:", e)
        short_reply = "Sorry, something went wrong."

    # 回复用户
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="Polly.Joanna">{short_reply}</Say>
</Response>"""
    return Response(twiml, mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
