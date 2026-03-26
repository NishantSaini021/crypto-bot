from pybit.unified_trading import HTTP
import requests
import time

    
# ====== YOUR DETAILS ======
API_KEY = "Jns0V7MYI0htUmCRtA6"
API_SECRET = "sgf8GGU6BtaWye9mruNdNFNc1wulimXLrxZH"

BOT_TOKEN = "8652456862:AAFrKQbOiK4HZDQns7dxMgROBqYPrEt16PU"

# ==========================
session = HTTP(api_key=API_KEY, api_secret=API_SECRET)

users = {}

def send_telegram(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": message})

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 100, "offset": offset}
    return requests.get(url, params=params).json()["result"]

print("Bot running...")

offset = None

while True:
    updates = get_updates(offset)

    for update in updates:
        offset = update["update_id"] + 1

        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")

            if text == "/start":
                send_telegram(chat_id, "Send me a price like 65000 and I’ll alert you.")
                continue

            try:
                target_price = float(text)
                users[chat_id] = target_price
                send_telegram(chat_id, f"✅ Alert set for {target_price}")
            except:
                send_telegram(chat_id, "❌ Send a valid number like 65000")

    try:
        ticker = session.get_tickers(category="linear", symbol="BTCUSDT")
        price = float(ticker['result']['list'][0]['lastPrice'])

        print("Price:", price)

        for chat_id, target in list(users.items()):
            if price >= target:
                send_telegram(chat_id, f"🚀 BTC reached {price}")
                del users[chat_id]

    except Exception as e:
        print("Error:", e)

    time.sleep(10)