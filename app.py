from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Kucoin auto trader is running."
