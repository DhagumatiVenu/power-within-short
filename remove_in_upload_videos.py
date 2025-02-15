import os



upload_videos = [f for f in os.listdir("upload_videos")]
uploaded_videos = "uploaded_videos"


for f in os.listdir(uploaded_videos):
    if f in upload_videos:
        s = os.path.join("upload_videos", f)
        os.remove(s)
        print("Removed", s)

