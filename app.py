from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "English Voice AI is running."

@app.route("/voice", methods=["POST"])
def voice():
    user_input = request.form.get("SpeechResult") or request.form.get("Body") or ""

    if user_input.strip() == "":
        # 👋 第一次通话，播报欢迎语
        ai_text = "Hello, how can I help you today?"
    else:
        try:
            chat_reply = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful and polite English-speaking voice assistant."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=150,
                temperature=0.6
            )
            ai_text = chat_reply["choices"][0]["message"]["content"][:300]  # 控制长度，防止中断
            print(f"✅ AI Reply: {ai_text}")
        except Exception as e:
            print(f"❌ OpenAI error: {e}")
            ai_text = "Sorry, something went wrong on my side."

    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna" language="en-US">{ai_text}</Say>
</Response>"""
    return Response(twiml_response, mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
