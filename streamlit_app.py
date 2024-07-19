import streamlit as st
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os

# Function to download YouTube video and convert to MP3
def download_and_convert(url, save_path):
    # Download YouTube video
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=save_path)
    
    # Convert to MP3
    video_clip = VideoFileClip(out_file)
    mp3_path = out_file.replace(".mp4", ".mp3")
    video_clip.audio.write_audiofile(mp3_path)
    
    # Cleanup
    os.remove(out_file)
    
    return mp3_path

# Streamlit app
def main():
    st.title("YouTube MP3 Downloader")
    
    url = st.text_input("Enter the YouTube URL:")
    if st.button("Download MP3"):
        if url:
            with st.spinner("Downloading and converting..."):
                save_path = "downloads"
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                
                mp3_path = download_and_convert(url, save_path)
                st.success(f"Download complete! Your MP3 file is available [here](./{mp3_path}).")
                st.audio(mp3_path)
        else:
            st.error("Please enter a valid YouTube URL.")

if __name__ == "__main__":
    main()
