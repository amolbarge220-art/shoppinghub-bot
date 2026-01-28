import time
import requests
import pytz
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler

# ====== CONFIG ======
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHANNEL = "@YourChannelUsername"
EARNKARO_API = "YOUR_EARNKARO_API_KEY"

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


from flask import Flask
import threading

app = Flask(name)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()
