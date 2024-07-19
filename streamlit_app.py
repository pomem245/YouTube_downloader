import streamlit as st
import yt_dlp
import os

def download_audio(link):
    with yt_dlp.YoutubeDL({'ignoreerrors':True, 'extract_audio': True, 'format': 'bestaudio', 'outtmpl': '%(title)s.mp3'}) as video:
        try:
            info_dict = video.extract_info(link, download = True)
            video_title = info_dict['title']
            return f"Successfully Downloaded: {video_title}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

st.title("YouTube Audio Downloader")

url = st.text_input("Paste YouTube link here:")

if st.button("Download Audio"):
    if url:
        with st.spinner("Downloading..."):
            result = download_audio(url)
        st.success(result)
    else:
        st.warning("Please enter a YouTube link.")

st.write("Note: This app downloads audio for personal use only. Respect copyright laws.")
