import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_USER_ID
from utils import set_trading_state, get_trading_state

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_USER_ID, "text": text}
    requests.post(url, data=payload)

def handle_telegram_commands(message_text):
    if message_text == "/start":
        send_telegram_message("👋 أهلاً بك في بوت KuCoin!\nاستخدم /help لعرض الأوامر.")

    elif message_text == "/help":
        send_telegram_message(
            "🛠️ أوامر البوت:\n"
            "/status - حالة البوت\n"
            "/last_trade - آخر صفقة\n"
            "/pause - إيقاف التداول\n"
            "/resume - استئناف التداول"
        )

    elif message_text == "/status":
        status = "✅ نشط" if get_trading_state() else "⏸️ متوقف"
        send_telegram_message(f"🔍 حالة البوت: {status}")

    elif message_text == "/pause":
        set_trading_state(False)
        send_telegram_message("⏸️ تم إيقاف التداول مؤقتًا.")

    elif message_text == "/resume":
        set_trading_state(True)
        send_telegram_message("✅ تم استئناف التداول.")

    elif message_text == "/last_trade":
        try:
            with open("trades.csv", "r") as f:
                lines = f.readlines()
                if len(lines) > 1:
                    last = lines[-1].strip().split(",")
                    msg = f"📈 آخر صفقة:\nزوج: {last[0]}\nدخول: {last[1]}\nخروج: {last[2]}\nكمية: {last[3]}\nربح/خسارة: {last[4]}%"
                else:
                    msg = "❗ لا توجد صفقات بعد."
        except:
            msg = "⚠️ تعذر قراءة الصفقات."
        send_telegram_message(msg)

    else:
        send_telegram_message("❓ أمر غير معروف. استخدم /help.")
