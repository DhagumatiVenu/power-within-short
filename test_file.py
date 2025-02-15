import requests

TELEGRAM_BOT_TOKEN = "7513376871:AAF6ZoG5Bc8SQF1WJruWDnDWN7o7e5SK5A0"

def get_updates():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    response = requests.get(url).json()
    print(response)  # Print all updates to find the chat ID

get_updates()
