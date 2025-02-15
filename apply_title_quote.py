import os
import multiprocessing
import pandas as pd
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip


videos = ['video_1.mp4', 'video_2.mp4', 'video_3.mp4', 'video_4.mp4', 'video_5.mp4', 'video_6.mp4', 'video_7.mp4', 'video_8.mp4', 'video_9.mp4', 'video_10.mp4', 'video_11.mp4', 'video_12.mp4', 'video_13.mp4', 'video_14.mp4', 'video_15.mp4', 'video_16.mp4', 'video_17.mp4', 'video_18.mp4', 'video_19.mp4', 'video_20.mp4', 'video_21.mp4', 'video_22.mp4', 'video_23.mp4', 'video_24.mp4', 'video_25.mp4', 'video_26.mp4', 'video_27.mp4', 'video_28.mp4', 'video_29.mp4', 'video_30.mp4', 'video_31.mp4', 'video_32.mp4', 'video_33.mp4', 'video_34.mp4', 'video_35.mp4', 'video_36.mp4', 'video_37.mp4', 'video_38.mp4', 'video_39.mp4', 'video_40.mp4', 'video_41.mp4', 'video_42.mp4', 'video_43.mp4', 'video_44.mp4', 'video_45.mp4', 'video_46.mp4', 'video_47.mp4', 'video_48.mp4', 'video_49.mp4', 'video_50.mp4', 'video_51.mp4', 'video_52.mp4', 'video_53.mp4', 'video_54.mp4', 'video_55.mp4', 'video_56.mp4', 'video_57.mp4', 'video_1.mp4', 'video_2.mp4', 'video_3.mp4', 'video_4.mp4', 'video_5.mp4', 'video_6.mp4', 'video_7.mp4', 'video_8.mp4', 'video_9.mp4', 'video_10.mp4', 'video_11.mp4', 'video_12.mp4', 'video_13.mp4', 'video_14.mp4', 'video_15.mp4', 'video_16.mp4', 'video_17.mp4', 'video_18.mp4', 'video_19.mp4', 'video_20.mp4', 'video_21.mp4', 'video_22.mp4', 'video_23.mp4', 'video_24.mp4', 'video_25.mp4', 'video_26.mp4', 'video_27.mp4', 'video_28.mp4', 'video_29.mp4', 'video_30.mp4', 'video_31.mp4', 'video_32.mp4', 'video_33.mp4', 'video_34.mp4', 'video_35.mp4', 'video_36.mp4', 'video_37.mp4', 'video_38.mp4', 'video_39.mp4', 'video_40.mp4', 'video_41.mp4', 'video_42.mp4', 'video_43.mp4', 'video_44.mp4', 'video_45.mp4', 'video_46.mp4', 'video_47.mp4', 'video_48.mp4', 'video_49.mp4', 'video_50.mp4', 'video_51.mp4', 'video_52.mp4', 'video_53.mp4', 'video_54.mp4', 'video_55.mp4', 'video_56.mp4', 'video_57.mp4', 'video_1.mp4', 'video_2.mp4', 'video_3.mp4', 'video_4.mp4', 'video_5.mp4', 'video_6.mp4', 'video_7.mp4', 'video_8.mp4', 'video_9.mp4', 'video_10.mp4', 'video_11.mp4', 'video_12.mp4', 'video_13.mp4', 'video_14.mp4', 'video_15.mp4', 'video_16.mp4', 'video_17.mp4', 'video_18.mp4', 'video_19.mp4', 'video_20.mp4', 'video_21.mp4', 'video_22.mp4', 'video_23.mp4', 'video_24.mp4', 'video_25.mp4', 'video_26.mp4', 'video_27.mp4', 'video_28.mp4', 'video_29.mp4', 'video_30.mp4', 'video_31.mp4', 'video_32.mp4', 'video_33.mp4', 'video_34.mp4', 'video_35.mp4', 'video_36.mp4', 'video_37.mp4', 'video_38.mp4', 'video_39.mp4', 'video_40.mp4', 'video_41.mp4', 'video_42.mp4', 'video_43.mp4', 'video_44.mp4', 'video_45.mp4', 'video_46.mp4', 'video_47.mp4', 'video_48.mp4', 'video_49.mp4', 'video_50.mp4', 'video_51.mp4', 'video_52.mp4', 'video_53.mp4', 'video_54.mp4', 'video_55.mp4', 'video_56.mp4', 'video_57.mp4', 'video_1.mp4', 'video_2.mp4', 'video_3.mp4', 'video_4.mp4', 'video_5.mp4', 'video_6.mp4', 'video_7.mp4', 'video_8.mp4', 'video_9.mp4', 'video_10.mp4', 'video_11.mp4', 'video_12.mp4', 'video_13.mp4', 'video_14.mp4', 'video_15.mp4', 'video_16.mp4', 'video_17.mp4', 'video_18.mp4', 'video_19.mp4', 'video_20.mp4', 'video_21.mp4', 'video_22.mp4', 'video_23.mp4', 'video_24.mp4', 'video_25.mp4', 'video_26.mp4', 'video_27.mp4', 'video_28.mp4', 'video_29.mp4']

os.environ["OMP_NUM_THREADS"] = str(multiprocessing.cpu_count())  # Adjust based on your CPU

# Input & output folders
input_folder = "videos"
output_folder = "upload_videos"
excel_file = "quotes.xlsx"  # Excel file with Titles & Quotes

# Load Excel file
df = pd.read_excel(excel_file)

# Loop through each row in the Excel file
for index, row in df.iterrows():
    title = row["Title"]  # Read title from Excel
    quote_text = row["Quote"]  # Read quote from Excel
    sanitized_title = "".join(c for c in title if c.isalnum() or c in " _-").strip()  # Remove special characters

    input_video = os.path.join(input_folder, videos[index])  # Assuming videos are named 1.mp4, 2.mp4...
    output_video = os.path.join(output_folder, f"{sanitized_title}.mp4")  # Use title as filename

    print(input_video)

    if os.path.exists(input_video):
        # Load video and remove audio
        final_video = VideoFileClip(input_video)

        # Create text clip for quote
        txt_clip1 = TextClip(txt=quote_text ,color="white", font="Arial",fontsize=40, method="caption", size=(900, None))
        txt_clip1 = txt_clip1.set_position(("center", 600)).set_duration(final_video.duration) # 50% down from the top
        txt_clip1 = txt_clip1.fadein(4)

        txt_clip2 = TextClip(txt="@powerwithin3809" ,color="white", fontsize=50, method="caption", size=(900, None))
        txt_clip2 = txt_clip2.set_position(("center", 1200)).set_duration(final_video.duration) # 50% down from the top
        txt_clip2 = txt_clip2.set_opacity(0.2)
        

        # Overlay text on video
        final_video = CompositeVideoClip([final_video, txt_clip1, txt_clip2])

        # Save final video (Keep original audio options)
        final_video.write_videofile(output_video, fps=30, codec="libx264")

        print(f"✅ Processed: {input_video} → Saved as {output_video}")

        # break # Remove it for batch processing.

print("🎥 All videos processed successfully!")

# a = []

# for i in videos:
#     a.append(i+".mp4")

# print(a)
