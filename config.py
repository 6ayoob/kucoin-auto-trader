import requests

def get_all_symbols():
    url = "https://api.kucoin.com/api/v1/symbols"
    response = requests.get(url)
    data = response.json()
    symbols = [
        item["symbol"] for item in data["data"]
        if item["enableTrading"] and item["quoteCurrency"] == "USDT" and item["market"] == "spot"
    ]
    return symbols

# KuCoin credentials
KUCOIN_API_KEY = "6877a82e28335c0001f580f0"
KUCOIN_API_SECRET = "da460f2e-b91e-483a-8aa4-02419bf1ab01"
KUCOIN_API_PASSPHRASE = "700110"

# Telegram Bot
TELEGRAM_BOT_TOKEN = "7708106993:AAHpd2Ceo7IQaeAHWiF3uUntKq7dJCPC9K0"
TELEGRAM_CHAT_ID = 658712542

# Trading Settings
TRADE_PERCENT = 10
STOP_LOSS_PERCENT = 5

# Automatically fetched spot symbols
SYMBOLS = get_all_symbols()
