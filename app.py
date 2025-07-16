from flask import Flask, request
from telegram_bot import handle_telegram_commands, send_telegram_message
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# تقرير يومي 4 م
scheduler = BackgroundScheduler()

def daily_report():
    send_telegram_message("📊 تقرير يومي:\n✅ البوت يعمل بشكل طبيعي.\n🕓 الوقت: 4 م")

scheduler.add_job(daily_report, 'cron', hour=13, minute=0)  # 13 UTC = 4 السعودية
scheduler.start()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.get_json()
        message = data.get("message", {}).get("text", "")
        handle_telegram_commands(message)
        return "OK"
    return "KuCoin Auto Trader Running ✅"

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
