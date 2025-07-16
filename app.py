from flask import Flask, request
from telegram_bot import handle_telegram_commands, send_telegram_message
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)
scheduler = BackgroundScheduler()

def report():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    send_telegram_message(f"📊 تقرير كل 3 ساعات:\n✅ البوت يعمل\n🕒 الوقت: {now}")

scheduler.add_job(report, 'interval', hours=3)
scheduler.start()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.get_json()
        message = data.get("message", {}).get("text", "")
        handle_telegram_commands(message)
        return "OK"
    return "KuCoin Auto Trader ✅"

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
