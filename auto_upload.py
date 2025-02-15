import os
import datetime
import time
import googleapiclient.discovery
import googleapiclient.errors
import google_auth_oauthlib.flow
import googleapiclient.http
import pytz
import requests
from titles import tags_hashtag_format, tags_comma_format
import shutil
import json

YOUTUBE_CREDENTIALS_JSON = os.getenv("YOUTUBE_CREDENTIALS")

if YOUTUBE_CREDENTIALS_JSON:
    with open("client_secrets.json", "w") as f:
        f.write(YOUTUBE_CREDENTIALS_JSON)

CLIENT_SECRETS_FILE = "client_secrets.json"


# Define YouTube API scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


# Authenticate and get credentials
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

# Ensure uploaded_videos folder exists
uploaded_folder = "uploaded_videos"
os.makedirs(uploaded_folder, exist_ok=True)

# Folder for the videos to upload
video_folder = "upload_videos"
video_files = [f for f in os.listdir(video_folder) if f.endswith(".mp4")]
    
# Function to send Telegram notifications
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"⚠ Telegram Error: {e}")

# For moving the video file into uploaded folder.
def move_video_safely(video_file):
        new_path = os.path.join(uploaded_folder, os.path.basename(video_file))
        shutil.copy(video_file, new_path)  # Copy first
        send_telegram_message(f"✅ Moved {video_file} to {uploaded_folder}")
        
# For deleting the uploaded video in the upload folder.
def delete_duplicate_video(video_file):
     os.remove(video_file)
     send_telegram_message(f"✅ Removed {video_file} in {video_folder}")

# Function to schedule video upload
def schedule_upload(video_file, title, description, tags, scheduled_time):
    try:
        request_body = {
            "snippet": {
                "title": title,
                "description": description + " " + tags_hashtag_format,
                "tags": tags,
                "categoryId": "22",
            },
            "status": {
                "privacyStatus": "private",
                "publishAt": scheduled_time
            }
        }

        media = googleapiclient.http.MediaFileUpload(video_file, chunksize=-1, resumable=True)
        request = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media)
        response = request.execute()

        video_link = f"https://www.youtube.com/watch?v={response['id']}"
        message = f"✅ Scheduled: {title} for {scheduled_time}\n🔗 Video Link: {video_link}"
        send_telegram_message(message)
        print(message)

        # Move uploaded video to uploaded_videos folder
        move_video_safely(video_file=video_file)
        time.sleep(2)
        delete_duplicate_video(video_file=video_file)

    except Exception as e:
        error_message = f"⚠ Error uploading {title}: {e}"
        send_telegram_message(error_message)
        print(error_message)

# Function to get tomorrow's scheduled time
def get_scheduled_time(hour, minute):
    timezone = pytz.timezone("Asia/Kolkata")  # Set your timezone
    now = datetime.datetime.now(timezone)
    scheduled_date = now + datetime.timedelta(days=1)
    scheduled_time = scheduled_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
    return scheduled_time.isoformat()


if len(video_files) >= 1:
    schedule_upload(
        os.path.join(video_folder, video_files[0]), 
        title=os.path.splitext(video_files[0])[0], 
        description="🔥 This is a powerful motivational video designed to ignite your inner strength and push you toward success. 💪✨", 
        tags=tags_comma_format, 
        scheduled_time=get_scheduled_time(8, 0)  # 8 AM
    )
    time.sleep(10)

# Send Telegram notification after processing all videos
send_telegram_message("✅ Video Schedules for next day.")

# Wait 24 hours before scheduling the next batch
time.sleep(86400)