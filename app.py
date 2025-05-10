from flask import Flask, request, Response
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/voice", methods=["POST"])
def voice():
    user_input = request.form.get("SpeechResult")
    
    if not user_input:
        # 第一次进来，先说一句话并等用户回应
        twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Gather input="speech" timeout="3" language="en-US">
    <Say>Hello, how can I help you?</Say>
  </Gather>
  <Say>I didn’t catch that. Goodbye!</Say>
</Response>"""
        return Response(twiml, mimetype="text/xml")

    # 有用户语音输入后，调用 ChatGPT 回复
    try:
        reply = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful voice assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        ai_text = reply.choices[0].message.content
    except Exception as e:
        print(f"OpenAI error: {e}")
        ai_text = "Sorry, there was an error."

    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say>{ai_text}</Say>
</Response>"""
    return Response(twiml_response, mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
