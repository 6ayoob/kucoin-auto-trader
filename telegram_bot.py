import requests
import os
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

def send_last_trade():
    try:
        with open("trades.csv", "r") as f:
            lines = f.readlines()
            if len(lines) >= 2:
                last_trade = lines[-1].strip()
                send_telegram_message(f"📈 آخر صفقة:\n{last_trade}")
            else:
                send_telegram_message("❌ لا يوجد صفقات مسجلة بعد.")
    except Exception as e:
        send_telegram_message(f"📛 حدث خطأ أثناء قراءة ملف الصفقات:\n{e}")

def handle_status_command():
    try:
        paused = os.path.exists("paused.txt")
        if paused:
            send_telegram_message("⏸️ التداول موقوف حاليًا.")
        else:
            send_telegram_message("✅ التداول مفعل ويعمل الآن.")
    except Exception as e:
        send_telegram_message(f"⚠️ حدث خطأ أثناء التحقق من حالة التداول:\n{e}")
