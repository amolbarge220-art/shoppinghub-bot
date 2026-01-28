import time
import requests
import pytz
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler

# ====== CONFIG ======
BOT_TOKEN = "8435541866:AAHf9HMgkVh6wTZWtPnhfeCrU0z5QQXcXq8"
CHANNEL = "@shoppinghubsmart"
EARNKARO_API = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2OTc5ZDI1YTA2MjRiMzJhNTc1ZjNhNjIiLCJlYXJua2FybyI6IjI5NjU3NTciLCJpYXQiOjE3Njk1OTMxOTl9.ROdW9fFWeftXZiXJqv42eJhTxB7oKUJGOKKPbtSMJFE"

bot = Bot(token=BOT_TOKEN)

# ====== FUNCTION ======
def fetch_and_post():
    url = f"https://api.earnkaro.com/deals?api_key={EARNKARO_API}"
    response = requests.get(url).json()

    for deal in response[:5]:
        if deal.get("discount", 0) >= 40:
            msg = f"""
🔥 *{deal['store']} Deal*

🛍 {deal['title']}
💸 {deal['discount']}% OFF
💰 Price: ₹{deal['price']}

👉 Buy Now: {deal['link']}

⚠️ Affiliate Link
"""
            bot.send_message(
                chat_id=CHANNEL,
                text=msg,
                parse_mode="Markdown"
            )

# ====== SCHEDULER ======
ist = pytz.timezone("Asia/Kolkata")

scheduler = BackgroundScheduler(timezone=ist)
scheduler.add_job(fetch_and_post, "interval", minutes=60)
scheduler.start()

print("🤖 Bot started successfully")

# ====== KEEP APP ALIVE (IMPORTANT FOR RENDER) ======
while True:
    time.sleep(60)
