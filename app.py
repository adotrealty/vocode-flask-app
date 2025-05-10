from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def home():
    return "Vocode Flask App is Running!"

@app.route("/voice", methods=["POST"])
def voice():
    return "<?xml version='1.0' encoding='UTF-8'?><Response><Say>Hello from Vocode Flask on Railway!</Say></Response>", 200, {"Content-Type": "application/xml"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
