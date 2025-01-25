import os
import re
import threading
# from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy import VideoFileClip,concatenate_videoclips

def process_clip(input_file, output_dir, start_time, end_time, clip_index,sample_video_path):

    try:
        print("----------------------Start cut movies.--------------------------------------")
            # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # # Load the main clip (5-minute segment)
        clip = VideoFileClip(input_file).subclipped(start_time, end_time)

        # Load the sample video
        sample_clip = VideoFileClip(sample_video_path)

        # Concatenate the sample video after the main clip
        clip = concatenate_videoclips([clip, sample_clip])
        
        # clip = VideoFileClip(input_file).subclipped(start_time, end_time)
        output_path = f"{output_dir}/{os.path.basename(input_file).split('.')[0]}_{clip_index}.mp4"
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac", bitrate="8000k", fps=60, threads=4)
        print(f"Saved: {output_path}")
        clip.close()
    except Exception as e:
        print(f"Error processing clip {clip_index}: {e}")


def split_video(input_file, output_dir, clip_duration=600):
    """
    Splits a video into smaller clips of specified duration.
    """
    try:
        video = VideoFileClip(input_file)
        total_duration = int(video.duration)
        start_time = 120
        clip_index = 0

        threads = []
                # Add sample video at the beginning of the video
        sample_clip = VideoFileClip("intro_video.mp4")
        # final_clips = [sample_clip]  #

        while start_time < total_duration:
            end_time = min(start_time + clip_duration, total_duration)
            process_clip(input_file, output_dir, start_time, end_time, clip_index,sample_clip)

            # thread = threading.Thread(target=process_clip, args=(input_file, output_dir, start_time, end_time, clip_index))
            
        #     thread.start()

        #     start_time = end_time
        #     clip_index += 1

        # for thread in threads:
        #     thread.join()

        video.close()
        sample_clip.close()
    except Exception as e:
        print(f"Error splitting video: {e}")

# --------------------------------------------------------------------------------------------
# import requests
# from datetime import datetime, timedelta
# import os
# import google.generativeai as genai
# import re

# # Facebook API credentials
# ACCESS_TOKEN = "your_facebook_access_token"  # Replace with your long-lived access token
# PAGE_ID = "your_page_id"  # Replace with your Facebook Page ID

# # Directory containing video files
# VIDEO_DIR = "path/to/your/videos"  # Replace with the directory containing your video files
# DESCRIPTION_TEMPLATE = "This is video post #{}! #Hashtag1 #Hashtag2"  # Template for video descriptions

# # Facebook Graph API URL for video uploads
# GRAPH_API_URL = f"https://graph.facebook.com/v16.0/{PAGE_ID}/videos"

# # Function to upload and schedule a video
# def upload_and_schedule_video(video_path, schedule_time, description):
#     with open(video_path, "rb") as video_file:
#         payload = {
#             "description": description,
#             "access_token": ACCESS_TOKEN,
#             "published": False,  # Ensure the video is not published immediately
#             "scheduled_publish_time": int(schedule_time.timestamp()),  # Unix timestamp
#         }
#         files = {"source": video_file}

#         response = requests.post(GRAPH_API_URL, data=payload, files=files)
#         if response.status_code == 200:
#             print(f"Video '{os.path.basename(video_path)}' scheduled successfully for {schedule_time}!")
#             print("Response:", response.json())
#         else:
#             print(f"Failed to schedule video '{os.path.basename(video_path)}'.")
#             print("Error:", response.json())

# def captions():
#     genai.configure(api_key="AIzaSyCLXEl-XKxZbPxatt2Dzmy-j83QWaO_2V0")

#     model_for_feedback = genai.GenerativeModel('gemini-1.0-pro')

#     prompt_feedback = f"generate 10 creative caption with emojis and relative popular hashtags from below sentence {generated_text}"

#     generate_caption = model_for_feedback.generate_content(prompt_feedback).text
#     # Split the string based on the numbers at the beginning of each sentence
#     caption_list = re.split(r'\d+\.', generate_caption)
#     return caption_list

# # Main function to schedule all videos
# def schedule_videos(file_path):
#     # Get all video files from the directory
#     video_files = [os.path.join(VIDEO_DIR, f) for f in os.listdir(VIDEO_DIR) if f.endswith((".mp4", ".mov"))]
#     video_files.sort()  # Sort files alphabetically or by name for consistent scheduling

#     # Start scheduling from the next available 11 AM
#     today = datetime.now()
#     next_11_am = today.replace(hour=11, minute=0, second=0, microsecond=0)
#     if today >= next_11_am:
#         next_11_am += timedelta(days=1)  # Move to the next day if today’s 11 AM has passed

#     # Schedule each video for the next available 11 AM slot
#     for index, video_path in enumerate(video_files):
#         schedule_time = next_11_am + timedelta(days=index)  # Increment by 1 day for each video
#         description = captions(video_path.split("/")[1].split("_")[0])  # Create a unique description for each video
#         upload_and_schedule_video(video_path, schedule_time, description)


# Run the script
if __name__ == "__main__":

    file_path = "Aladdin.mkv"  # Replace with your video file path
    output_dir = file_path.split(".mkv")[0] # Replace with your desired output directory
    split_video(file_path, output_dir)

    # Upload To Facebook
    # from facebook_upload import schedule_videos
    # schedule_videos(output_dir)
