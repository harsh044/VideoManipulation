import requests
from datetime import datetime, timedelta
import os
import google.generativeai as genai
import re

# Facebook API credentials
ACCESS_TOKEN = "your_facebook_access_token"  # Replace with your long-lived access token
PAGE_ID = "your_page_id"  # Replace with your Facebook Page ID

# Directory containing video files
VIDEO_DIR = "path/to/your/videos"  # Replace with the directory containing your video files
DESCRIPTION_TEMPLATE = "This is video post #{}! #Hashtag1 #Hashtag2"  # Template for video descriptions

# Facebook Graph API URL for video uploads
GRAPH_API_URL = f"https://graph.facebook.com/v16.0/{PAGE_ID}/videos"

# Function to upload and schedule a video
def upload_and_schedule_video(video_path, schedule_time, description):
    with open(video_path, "rb") as video_file:
        payload = {
            "description": description,
            "access_token": ACCESS_TOKEN,
            "published": False,  # Ensure the video is not published immediately
            "scheduled_publish_time": int(schedule_time.timestamp()),  # Unix timestamp
        }
        files = {"source": video_file}

        response = requests.post(GRAPH_API_URL, data=payload, files=files)
        if response.status_code == 200:
            print(f"Video '{os.path.basename(video_path)}' scheduled successfully for {schedule_time}!")
            print("Response:", response.json())
        else:
            print(f"Failed to schedule video '{os.path.basename(video_path)}'.")
            print("Error:", response.json())

def captions():
    genai.configure(api_key="AIzaSyCLXEl-XKxZbPxatt2Dzmy-j83QWaO_2V0")

    model_for_feedback = genai.GenerativeModel('gemini-1.0-pro')

    prompt_feedback = f"generate 10 creative caption with emojis and relative popular hashtags from below sentence {generated_text}"

    generate_caption = model_for_feedback.generate_content(prompt_feedback).text
    # Split the string based on the numbers at the beginning of each sentence
    caption_list = re.split(r'\d+\.', generate_caption)
    return caption_list

# Main function to schedule all videos
def schedule_videos(file_path):
    # Get all video files from the directory
    video_files = [os.path.join(VIDEO_DIR, f) for f in os.listdir(VIDEO_DIR) if f.endswith((".mp4", ".mov"))]
    video_files.sort()  # Sort files alphabetically or by name for consistent scheduling

    # Start scheduling from the next available 11 AM
    today = datetime.now()
    next_11_am = today.replace(hour=11, minute=0, second=0, microsecond=0)
    if today >= next_11_am:
        next_11_am += timedelta(days=1)  # Move to the next day if today’s 11 AM has passed

    # Schedule each video for the next available 11 AM slot
    for index, video_path in enumerate(video_files):
        schedule_time = next_11_am + timedelta(days=index)  # Increment by 1 day for each video
        description = captions(video_path.split("/")[1].split("_")[0])  # Create a unique description for each video
        upload_and_schedule_video(video_path, schedule_time, description)
