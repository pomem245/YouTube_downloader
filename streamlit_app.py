import streamlit as st
import yt_dlp
import os

def download_audio(link):
    """Download audio from a given YouTube link and return the file path."""
    output_file = f"{link.split('=')[-1]}.mp3"  # Generate a filename based on the video ID
    ydl_opts = {
        'ignoreerrors': True,
        'extract_audio': True,
        'format': 'bestaudio',
        'outtmpl': output_file,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(link, download=True)
            video_title = info_dict['title']
            return output_file, video_title
        except Exception as e:
            return None, str(e)

st.title("YouTube Audio Downloader")

url = st.text_input("Paste YouTube link here:")

if url:
    with st.spinner("Downloading..."):
        file_path, message = download_audio(url)
    
    if file_path:
        st.success(f"Successfully downloaded: {message}")
        with open(file_path, "rb") as audio_file:
            st.download_button(
                label="Download Audio File",
                data=audio_file,
                file_name=os.path.basename(file_path),
                mime="audio/mpeg"
            )
        # Optionally, remove the file after download
        # os.remove(file_path)
    else:
        st.error(f"An error occurred: {message}")

st.write("Note: This app downloads audio for personal use only. Respect copyright laws.")
