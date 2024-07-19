import streamlit as st
from pytube import YouTube, Playlist
import re
import os
from concurrent.futures import ThreadPoolExecutor

class YouTubeDownloader:
    def __init__(self):
        self.save_path = "downloads"
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def start_download(self, urls):
        urls = [url.strip() for url in urls if url.strip()]
        
        if not urls:
            st.error("Please enter at least one YouTube URL")
            return

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.download_url, url) for url in urls]
            for i, future in enumerate(futures):
                future.result()  # Wait for all downloads to complete
                st.progress(int((i + 1) / len(urls) * 100))
        
        st.success("Download complete")

    def download_url(self, url):
        try:
            if 'playlist' in url:
                playlist = Playlist(url)
                for video in playlist.videos:
                    self.download_video(video)
            else:
                video = YouTube(url)
                self.download_video(video)
        except Exception as e:
            st.error(f"Error: {e}")

    def download_video(self, video):
        stream = video.streams.filter(only_audio=True).first()
        sanitized_title = self.sanitize_filename(video.title)
        stream.download(output_path=self.save_path, filename=f"{sanitized_title}.mp3")

    def sanitize_filename(self, filename):
        return re.sub(r'[<>:"/\\|?*]', '', filename)


# Streamlit UI
st.title('YouTube MP3 Downloader')

st.write('Enter YouTube URL(s) (one per line or playlist URL):')
urls = st.text_area('Enter URLs here...')

if st.button('Download MP3'):
    downloader = YouTubeDownloader()
    downloader.start_download(urls.split('\n'))

# Display the downloaded files
download_folder = "downloads"
if os.path.exists(download_folder):
    st.write("Downloaded files:")
    files = os.listdir(download_folder)
    for file in files:
        with open(os.path.join(download_folder, file), "rb") as f:
            st.download_button(
                label=f"Download {file}",
                data=f.read(),
                file_name=file,
                mime="audio/mpeg"
            )
