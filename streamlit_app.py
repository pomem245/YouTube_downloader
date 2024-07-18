import streamlit as st
import re
from pytube import YouTube, Playlist
import os
from concurrent.futures import ThreadPoolExecutor
import zipfile
import tempfile
import io

class YouTubeDownloader:
    def __init__(self):
        self.save_path = ""

    def download_url(self, url):
        downloaded_files = []
        try:
            if 'playlist' in url:
                playlist = Playlist(url)
                for video in playlist.videos:
                    file_path = self.download_video(video)
                    if file_path:
                        downloaded_files.append(file_path)
            else:
                video = YouTube(url)
                file_path = self.download_video(video)
                if file_path:
                    downloaded_files.append(file_path)
        except Exception as e:
            st.error(f"Error with URL {url}: {e}")
        return downloaded_files

    def download_video(self, video):
        try:
            stream = video.streams.filter(only_audio=True).first()
            sanitized_title = self.sanitize_filename(video.title)
            file_path = os.path.join(self.save_path, f"{sanitized_title}.mp3")
            stream.download(output_path=self.save_path, filename=f"{sanitized_title}.mp3")
            return file_path
        except Exception as e:
            st.error(f"Error downloading video {video.title}: {e}")
            return None

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

        with tempfile.TemporaryDirectory() as temp_dir:
            downloader.save_path = temp_dir
            progress_bar = st.progress(0)
            status_text = st.empty()
            all_downloaded_files = []

            with ThreadPoolExecutor() as executor:
                futures = {executor.submit(downloader.download_url, url): url for url in url_list}
                for i, future in enumerate(futures):
                    downloaded_files = future.result()  # Get downloaded files
                    all_downloaded_files.extend(downloaded_files)
                    progress = int((i + 1) / len(url_list) * 100)
                    progress_bar.progress(progress)
                    status_text.text(f"Downloading... {progress}%")

            if all_downloaded_files:
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                    for file_path in all_downloaded_files:
                        zip_file.write(file_path, os.path.basename(file_path))
                zip_buffer.seek(0)
                st.download_button(
                    label="Download MP3 Files",
                    data=zip_buffer,
                    file_name="downloaded_mp3s.zip",
                    mime="application/zip"
                )
                st.success("Download complete")
            else:
                st.error("No files downloaded")

if __name__ == "__main__":
    main()
