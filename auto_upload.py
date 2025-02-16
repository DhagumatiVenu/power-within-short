import os
import datetime
import time
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http
import google_auth_oauthlib.flow
from google.oauth2.credentials import Credentials
from titles import tags_comma_format, tags_hashtag_format
import pytz
import requests
import shutil

# Load YouTube Credentials from GitHub Secrets
CREDENTIALS_FILE = "credentials.json"
YOUTUBE_CREDENTIALS_JSON = os.getenv("YOUTUBE_CREDENTIALS")

if YOUTUBE_CREDENTIALS_JSON:
    with open(CREDENTIALS_FILE, "w") as f:
        f.write(YOUTUBE_CREDENTIALS_JSON)

if os.path.exists(CREDENTIALS_FILE):
    credentials = Credentials.from_authorized_user_file(CREDENTIALS_FILE)
else:
    raise Exception("⚠ Missing YouTube API credentials. Authenticate locally first.")

# Initialize YouTube API
youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

# Load Telegram Credentials
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = str(int(os.getenv("TELEGRAM_CHAT_ID"))*-1)

# Ensure uploaded_videos folder exists
uploaded_folder = "uploaded_videos"
os.makedirs(uploaded_folder, exist_ok=True)

# Folder for the videos to upload
video_folder = "upload_videos"
video_files = [f for f in os.listdir(video_folder) if f.endswith(".mp4")]
video_file = os.path.join(video_folder, video_files[0])

# Function to send Telegram notifications
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"⚠ Telegram Error: {e}")

# Move uploaded videos to archive folder
def move_video_safely(video_file):
    try:
        new_path = os.path.join(uploaded_folder, os.path.basename(video_file))
        shutil.move(video_file, new_path)
        send_telegram_message(f"✅ Moved {video_file} to {uploaded_folder}")
    except Exception as e:
        send_telegram_message(f"❌ Error moving {video_file} to {uploaded_folder}")

# Function to schedule YouTube video upload
def schedule_upload(video_file, title, description, tags, scheduled_time):
    try:
        request_body = {
            "snippet": {
                "title": title,
                "description": description+" "+tags_hashtag_format,
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

    except Exception as e:
        error_message = f"venu: Error uploading {title}: {e}"
        send_telegram_message(error_message)
        

# Function to get the scheduled upload time
def get_scheduled_time(hour, minute):
    timezone = pytz.timezone("Asia/Kolkata")
    now = datetime.datetime.now(timezone)
    scheduled_date = now + datetime.timedelta(days=1)
    scheduled_time = scheduled_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
    return scheduled_time.isoformat()

# Upload the first video in the list
if len(video_files) >= 1:
    schedule_upload(
        video_file=video_file, 
        title=os.path.splitext(video_files[0])[0], 
        description="🔥 A powerful motivational video to ignite your inner strength. 💪✨", 
        tags=tags_comma_format,  # Modify tags as needed
        scheduled_time=get_scheduled_time(8, 0)
    )
    move_video_safely(video_file)
    