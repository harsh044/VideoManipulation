import os
import re
import threading
from moviepy import VideoFileClip,concatenate_videoclips

def process_clip(input_file, output_dir, start_time, end_time, clip_index, sample_video_path):
    try:
        print("----------------------Start cutting movies.--------------------------------------")

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Load the main clip (5-minute segment)
        clip = VideoFileClip(input_file).subclip(start_time, end_time)

        # Load the sample video
        sample_clip = VideoFileClip(sample_video_path)

        # Concatenate the sample video after the main clip
        final_clip = concatenate_videoclips([clip, sample_clip])

        output_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_{clip_index}.mp4")
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", bitrate="8000k", fps=60, threads=4)

        print(f"Saved: {output_path}")
        final_clip.close()
    except Exception as e:
        print(f"Error processing clip {clip_index}: {e}")

def split_video(input_file, output_dir, clip_duration=600):
    """
    Splits a video into smaller clips of specified duration and appends a sample video.
    """
    try:
        video = VideoFileClip(input_file)
        total_duration = int(video.duration)
        start_time = 120
        clip_index = 0

        # Path to the sample video
        sample_video_path = "intro_video.mp4"

        while start_time < total_duration:
            end_time = min(start_time + clip_duration, total_duration)
            process_clip(input_file, output_dir, start_time, end_time, clip_index, sample_video_path)

            start_time = end_time
            clip_index += 1

        video.close()
    except Exception as e:
        print(f"Error splitting video: {e}")

if __name__ == "__main__":
    file_path = "Aladdin.mkv"  # Replace with your video file path
    output_dir = os.path.splitext(file_path)[0]  # Directory named after the video file (without extension)
    split_video(file_path, output_dir)
