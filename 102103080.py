#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import shutil
import argparse
import yt_dlp
from moviepy.editor import VideoFileClip, concatenate_audioclips

def download_videos(singer, n):
    url = f"https://www.youtube.com/results?search_query={singer}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'outtmpl': f'downloads/{singer}-%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info_dict)

def convert_to_audio(video_path, output_path):
    clip = VideoFileClip(video_path)
    audio_clip = clip.audio
    audio_clip.write_audiofile(output_path)

def cut_audio(input_path, output_path, duration):
    audio_clip = AudioFileClip(input_path).subclip(0, duration)
    audio_clip.write_audiofile(output_path)

def merge_audios(audio_files, output_path):
    clips = [AudioFileClip(file) for file in audio_files]
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_path)

def clean_up():
    shutil.rmtree("downloads")


# In[3]:


def main():
    try:
        parser = argparse.ArgumentParser(description="YouTube Video Processing")
        parser.add_argument("singer", help="Name of the singer")
        parser.add_argument("n", type=int, help="Number of videos to download (N > 10)")
        parser.add_argument("duration", type=int, help="Duration to cut from each video (Y > 20)")
        args = parser.parse_args()

        singer = args.singer
        n = args.n
        duration = args.duration

        if n <= 10 or duration <= 20:
            raise ValueError("Please provide values greater than 10 for N and 20 for Y.")

        os.makedirs("downloads", exist_ok=True)

        videos = download_videos(singer, n)

        audio_files = []
        for i in range(1, n+1):
            video_path = f"downloads/{singer}-{i}.mp4"
            audio_path = f"downloads/{singer}-{i}.mp3"
            cut_audio_path = f"downloads/{singer}-{i}_cut.mp3"

            convert_to_audio(video_path, audio_path)
            cut_audio(audio_path, cut_audio_path, duration)

            audio_files.append(cut_audio_path)

        output_path = f"downloads/{singer}_output.mp3"
        merge_audios(audio_files, output_path)

        print(f"All tasks completed. Merged audio saved at: {output_path}")

        clean_up()

    except Exception as e:
        import traceback
        traceback.print_exc()
        clean_up()

if __name__ == "__main__":
    main()


# In[ ]:




