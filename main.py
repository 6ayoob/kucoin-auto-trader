from flask import Flask, request
from telegram_bot import send_message, handle_command
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 KuCoin Auto-Trader is Live!"

@app.route(f"/{os.getenv('TELEGRAM_BOT_TOKEN')}", methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        handle_command(chat_id, text)
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
