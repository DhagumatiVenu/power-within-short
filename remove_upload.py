import os
import requests

# Load Telegram Credentials
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = str(int(os.getenv("TELEGRAM_CHAT_ID"))*-1)

# Define folders
upload_videos_folder = "upload_videos"
uploaded_videos_folder = "uploaded_videos"

# Function to send Telegram notifications
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"⚠ Telegram Error: {e}")

# Function to delete uploaded videos from `upload_videos`
def remove_uploaded_videos():
    upload_videos = set(os.listdir(upload_videos_folder))
    uploaded_videos = set(os.listdir(uploaded_videos_folder))

    deleted_count = 0

    for video in uploaded_videos:
        if video in upload_videos:
            try:
                video_path = os.path.join(upload_videos_folder, video)
                os.remove(video_path)
                send_telegram_message(f"✅ Removed {video} from {upload_videos_folder}")
                print(f"✅ Successfully deleted {video}")
                deleted_count += 1
            except Exception as e:
                send_telegram_message(f"⚠ Error deleting {video}: {e}")
                print(f"⚠ Error deleting {video}: {e}")

    if deleted_count == 0:
        send_telegram_message("⚠ No matching videos found to delete.")

# Run the delete function
remove_uploaded_videos()
