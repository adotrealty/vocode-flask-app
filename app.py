from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    # TwiML with <Gather> to wait for user's voice input
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather input="speech" timeout="5" language="en-US">
        <Say voice="Polly.Joanna">Hello, how can I help you?</Say>
    </Gather>
    <Say voice="Polly.Joanna">Sorry, I didn't catch that. Goodbye!</Say>
</Response>"""
    return Response(twiml, mimetype="text/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
