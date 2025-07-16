from flask import Flask, request
from telegram_bot import send_telegram_message, send_last_trade, handle_status_command
from kucoin_client import check_market
import os

# إدراج التوكن ومعرف التيليجرام مباشرة
TELEGRAM_BOT_TOKEN = "7863509137:AAHBuRbtzMAOM_yBbVZASfx-oORubvQYxY8"
TELEGRAM_CHAT_ID = 658712542  # غيّره إذا كان هناك معرف مختلف

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ KuCoin Auto-Trader is Live!"

@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def telegram_webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if chat_id != TELEGRAM_CHAT_ID:
            return "unauthorized", 403

        if text == "/start":
            send_telegram_message("🤖 مرحباً بك في بوت KuCoin Auto-Trader!\nاكتب /help لرؤية الأوامر.")
        elif text == "/help":
            send_telegram_message(
                "📘 أوامر البوت:\n"
                "/start - بدء البوت\n"
                "/help - قائمة الأوامر\n"
                "/status - حالة البوت الآن\n"
                "/scan - فحص السوق الآن\n"
                "/last - عرض آخر صفقة\n"
                "/pause - إيقاف التداول مؤقتًا\n"
                "/resume - استئناف التداول"
            )
        elif text == "/status":
            handle_status_command()
        elif text == "/scan":
            check_market()
        elif text == "/last":
            send_last_trade()
        elif text == "/pause":
            with open("paused.txt", "w") as f:
                f.write("true")
            send_telegram_message("⏸️ تم إيقاف التداول مؤقتًا.")
        elif text == "/resume":
            if os.path.exists("paused.txt"):
                os.remove("paused.txt")
            send_telegram_message("▶️ تم استئناف التداول.")
        else:
            send_telegram_message("❓ أمر غير معروف. اكتب /help لعرض الأوامر.")

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
