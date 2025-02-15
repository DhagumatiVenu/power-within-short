import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx, AudioFileClip
import multiprocessing

os.environ["OMP_NUM_THREADS"] = str(multiprocessing.cpu_count())  # Adjust based on your CPU

# Input & output folders
input_folder = "original_folder"
output_folder = "videos"
quote_text = "Your only limit is you."  # Change this for each video

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

i = 1
for filename in os.listdir(input_folder):
    if filename.endswith(".mp4"):
        input_video = os.path.join(input_folder, filename)
        output_video = os.path.join(output_folder, f"video_{i}.mp4")

        # Load video and remove audio
        video = VideoFileClip(input_video).without_audio()

        # Trim if longer than 11 sec, otherwise loop
        if video.duration >= 11:
            final_video = video.subclip(0, 11)
        else:
            clips = []
            while sum([clip.duration for clip in clips]) < 11:
                clips.append(video)
            final_video = concatenate_videoclips(clips).subclip(0, 11)

        # Resize to YouTube Shorts format (1080x1920)
        final_video = final_video.resize((1080, 1920))

        # Reduce brightness (Multiply by a factor < 1 to darken)
        final_video = final_video.fx(vfx.colorx, 0.1)  # 0.2 makes it darker

        # Load background music, trim to 11 sec & reduce volume by 50%
        audio = AudioFileClip("music_1.mp3").subclip(0, 11).volumex(0.5)

        # Attach modified music to video
        final_video = final_video.set_audio(audio)

        # Save final video
        final_video.write_videofile(output_video, fps=30, codec="libx264", audio_codec="aac")

        print(f"✅ Processed: {filename} → Saved as {output_video}")

        i += 1

        # break  # Remove this if processing all videos

print("🎥 All videos processed successfully!")
