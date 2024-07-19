import streamlit as st
from pytube import YouTube, Playlist
import re
from concurrent.futures import ThreadPoolExecutor
import os

# Function to sanitize filenames
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

# Function to download video as audio
def download_video(video, save_path):
    stream = video.streams.filter(only_audio=True).first()
    sanitized_title = sanitize_filename(video.title)
    filepath = os.path.join(save_path, f"{sanitized_title}.mp3")
    stream.download(output_path=save_path, filename=f"{sanitized_title}.mp3")
    return filepath

# Function to download URL
def download_url(url, save_path):
    try:
        if 'playlist' in url:
            playlist = Playlist(url)
            return [download_video(video, save_path) for video in playlist.videos]
        else:
            video = YouTube(url)
            return [download_video(video, save_path)]
    except Exception as e:
        st.error(f"Error: {e}")
        return []

# Streamlit UI
st.title('YouTube Downloader')

url_input = st.text_area('Enter YouTube URL(s) (one per line or playlist URL):', height=150)
save_path = st.text_input('Enter Save Location:', value=os.getcwd())
download_button = st.button('Download MP3')

if download_button:
    urls = url_input.strip().split('\n')
    urls = [url.strip() for url in urls if url.strip()]

    if not urls:
        st.error("Please enter at least one YouTube URL")
    elif not save_path:
        st.error("Please enter a save location")
    else:
        with st.spinner('Downloading...'):
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(download_url, url, save_path) for url in urls]
                results = []
                for future in futures:
                    results.extend(future.result())

            st.success("Download complete")

        # Provide download links for each file
        for result in results:
            if result:
                for file in result:
                    st.markdown(f"[Download {os.path.basename(file)}](file://{file})")

