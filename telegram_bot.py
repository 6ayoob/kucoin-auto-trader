import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_USER_ID

# إرسال رسالة إلى Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_USER_ID,
        "text": text
    }
    requests.post(url, data=payload)

# تحليل الأوامر
def handle_telegram_commands(message_text):
    if message_text == "/start":
        send_telegram_message(
            "👋 أهلاً بك في بوت KuCoin الآلي!\n"
            "استخدم /help لعرض الأوامر المتاحة."
        )

    elif message_text == "/help":
        send_telegram_message(
            "🛠️ أوامر البوت:\n"
            "/status - عرض حالة البوت الحالية\n"
            "/last_trade - عرض آخر صفقة تمت\n"
            "/help - عرض هذه القائمة"
        )

    elif message_text == "/status":
        send_telegram_message(
            "🤖 البوت يعمل ✅\n"
            "📊 الاستراتيجية: MACD\n"
            "🔄 التداول كل 10 دقائق\n"
            "📅 التقرير اليومي يتم إرساله 4م"
        )

    elif message_text == "/last_trade":
        try:
            with open("trades.csv", "r") as f:
                lines = f.readlines()
                if len(lines) > 1:
                    last = lines[-1].strip().split(",")
                    msg = f"📈 آخر صفقة:\nزوج: {last[0]}\nسعر: {last[1]}\nكمية: {last[2]}\nوقت: {last[3]}"
                else:
                    msg = "❗ لا توجد صفقات مسجلة بعد."
        except:
            msg = "❗ لا يمكن قراءة ملف التداولات."
        send_telegram_message(msg)

    else:
        send_telegram_message("❓ أمر غير معروف. استخدم /help لعرض الأوامر.")

