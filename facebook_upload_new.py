import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re

# Load environment variables from .env file
load_dotenv()

# Facebook API credentials
ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")  # Retrieved from .env
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")  # Retrieved from .env

# Directory containing video files
VIDEO_DIR = os.getenv("VIDEO_DIR")  # Retrieved from .env

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
    genai.configure(api_key=os.getenv("GENAI_API_KEY"))  # Retrieved from .env

    model_for_feedback = genai.GenerativeModel('gemini-1.0-pro')

    prompt_feedback = "Generate 10 creative captions with emojis and relative popular hashtags from below sentence."

    generate_caption = model_for_feedback.generate_content(prompt_feedback).text
    # Split the string based on the numbers at the beginning of each sentence
    caption_list = re.split(r'\d+\.', generate_caption)
    return caption_list

# Main function to schedule all videos
def schedule_videos():
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
        description = captions(video_path.split("/")[1].split("_")[0])  # Create a unique description for eachn
        upload_and_schedule_video(video_path, schedule_time, description)

if __name__ == "__main__":
    schedule_videos()
