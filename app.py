from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Twilio AI Voice Assistant is running."

@app.route("/voice", methods=["POST"])
def voice():
    user_input = request.form.get("SpeechResult")

    if not user_input:
        # 第一次通话，引导语音输入
        twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Gather input="speech" timeout="3" language="en-US">
    <Say voice="Polly.Joanna">Hello, how can I help you?</Say>
  </Gather>
  <Say voice="Polly.Joanna">I didn’t catch that. Goodbye!</Say>
</Response>"""
        return Response(twiml, mimetype="text/xml")

    try:
        print("🎤 User said:", user_input)

        # ChatGPT 回复，限制长度
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly and concise AI voice assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=100,
            temperature=0.6
        )

        full_reply = completion["choices"][0]["message"]["content"]
        short_reply = full_reply.strip().split(".")[0] + "."  # 截取第一句话
        print("🤖 AI reply:", short_reply)

    except Exception as e:
        print("OpenAI error:", e)
        short_reply = "Sorry, something went wrong."

    # 播放回应前加提示，减少冷场
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="Polly.Joanna">Let me answer that.</Say>
  <Pause length="1"/>
  <Say voice="Polly.Joanna">{short_reply}</Say>
</Response>"""
    return Response(twiml, mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
