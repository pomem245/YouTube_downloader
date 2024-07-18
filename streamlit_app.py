import streamlit as st
import re
from pytube import YouTube, Playlist
import os
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

class YouTubeDownloader:
    def __init__(self):
        self.files = []

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
            st.error(f"Error with URL {url}: {e}")

    def download_video(self, video):
        try:
            stream = video.streams.filter(only_audio=True).first()
            sanitized_title = self.sanitize_filename(video.title)
            buffer = BytesIO()
            stream.stream_to_buffer(buffer)
            buffer.seek(0)
            self.files.append((f"{sanitized_title}.mp3", buffer.read()))
        except Exception as e:
            st.error(f"Error downloading video {video.title}: {e}")

    def sanitize_filename(self, filename):
        return re.sub(r'[<>:"/\\|?*]', '', filename)

def main():
    st.title("YouTube MP3 Downloader")

    downloader = YouTubeDownloader()

    urls = st.text_area("Enter YouTube URL(s) (one per line or playlist URL):", height=100)

    if st.button("Download MP3"):
        if not urls.strip():
            st.error("Please enter at least one YouTube URL")
            return

        url_list = [url.strip() for url in urls.strip().split('\n') if url.strip()]

        progress_bar = st.progress(0)
        status_text = st.empty()

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(downloader.download_url, url): url for url in url_list}
            for i, future in enumerate(futures):
                future.result()  # Wait for all downloads to complete
                progress = int((i + 1) / len(url_list) * 100)
                progress_bar.progress(progress)
                status_text.text(f"Downloading... {progress}%")

        st.success("Download complete")

        for filename, file_content in downloader.files:
            st.download_button(label=f"Download {filename}",
                               data=file_content,
                               file_name=filename,
                               mime='audio/mpeg')

if __name__ == "__main__":
    main()
