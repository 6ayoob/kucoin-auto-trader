import requests

# توكن البوت
TOKEN = "7708106993:AAHpd2Ceo7IQaeAHWif3uUntKq7dJCPC9K0"

# رابط مشروعك على Render (غيره إلى رابط مشروعك الحقيقي)
WEBHOOK_URL = f"https://kucoin-auto-trader.onrender.com/{TOKEN}"

# طلب تعيين Webhook
response = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}")

# طباعة النتيجة
print(response.json())
