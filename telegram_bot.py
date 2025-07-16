import os
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")

def handle_command(chat_id, text):
    if str(chat_id) != str(TELEGRAM_CHAT_ID):
        return

    if text == "/start":
        send_message("🤖 *مرحبًا بك في KuCoin Auto-Trader!*")
    elif text == "/help":
        send_message("""📘 *الأوامر المتاحة:*
/start - بدء البوت
/help - عرض هذه القائمة
/status - حالة البوت
/last - آخر صفقة
/pause - إيقاف التداول مؤقتًا
/resume - استئناف التداول""")
    elif text == "/status":
        if os.path.exists("paused.txt"):
            send_message("⏸️ *التداول متوقف حاليًا.*")
        else:
            send_message("✅ *التداول نشط.*")
    elif text == "/pause":
        open("paused.txt", "w").close()
        send_message("⏸️ *تم إيقاف التداول مؤقتًا.*")
    elif text == "/resume":
        if os.path.exists("paused.txt"):
            os.remove("paused.txt")
        send_message("▶️ *تم استئناف التداول.*")
    elif text == "/last":
        try:
            with open("trades.csv", "r") as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    send_message(f"📈 *آخر صفقة:*
{lines[-1]}")
                else:
                    send_message("⚠️ لا يوجد صفقات مسجلة.")
        except:
            send_message("⚠️ لا يمكن قراءة ملف الصفقات.")
    else:
        send_message("❓ *أمر غير معروف. اكتب /help لعرض الأوامر.*")
