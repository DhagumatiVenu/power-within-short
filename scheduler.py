import requests
import schedule
import time

# 🔹 Replace with your bot token & chat ID
TELEGRAM_BOT_TOKEN = "7513376871:AAF6ZoG5Bc8SQF1WJruWDnDWN7o7e5SK5A0"
TELEGRAM_CHAT_ID = "-4744121235"

# 🔹 Function to send a Telegram message
def power_within_short():
    message = "🎥 Upload Your Video\n🔗 Link : "
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

    try:
        response = requests.post(url, json=payload)
        print(f"✅ Notification Sent: {response.json()}")
    except Exception as e:
        print(f"⚠ Telegram Error: {e}")

# 🔹 Schedule the notification (set to 9 AM daily)
schedule.every().day.at("12:00").do(power_within_short)

# 🔹 Keep the script running
print("🚀 Telegram bot is running...")
while True:
    schedule.run_pending()
    time.sleep(60)  # Wait 1 minute before checking again
