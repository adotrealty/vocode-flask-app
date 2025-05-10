@app.route("/voice", methods=["POST"])
def voice():
    # 固定一句内容测试连通性
    user_input = "请你介绍一下你自己"

    try:
        chat_reply = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个温和的中文语音助手"},
                {"role": "user", "content": user_input}
            ]
        )
        ai_text = chat_reply["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"OpenAI error: {e}")
        ai_text = "很抱歉，我刚才好像出错了。"

    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="zh-CN" voice="Alice">{ai_text}</Say>
</Response>"""
    return Response(twiml_response, mimetype="text/xml")
