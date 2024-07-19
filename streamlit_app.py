import streamlit as st
import re
from pytube import YouTube, Playlist
import os
from concurrent.futures import ThreadPoolExecutor

class YouTubeDownloader:
    def __init__(self):
        self.save_path = "downloads"
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        
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
        file_path = os.path.join(self.save_path, f"{sanitized_title}.mp3")
        stream.download(output_path=self.save_path, filename=f"{sanitized_title}.mp3")
        return file_path

    def sanitize_filename(self, filename):
        return re.sub(r'[<>:"/\\|?*]', '', filename)

def main():
    st.title("YouTube MP3 Downloader")

    downloader = YouTubeDownloader()

    urls = st.text_area("Enter YouTube URL(s) (one per line or playlist URL):", placeholder="Enter URLs here...")
    
    if st.button("Download MP3"):
        if not urls:
            st.warning("Please enter at least one YouTube URL")
        else:
            url_list = urls.strip().split('\n')
            url_list = [url.strip() for url in url_list if url.strip()]
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            downloaded_files = []
            
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(downloader.download_url, url) for url in url_list]
                for i, future in enumerate(futures):
                    file_path = future.result()
                    if file_path:
                        downloaded_files.append(file_path)
                    progress = int((i + 1) / len(url_list) * 100)
                    progress_bar.progress(progress)
                    status_text.text(f"Downloading... {progress}%")
            
            status_text.text("Download complete!")
            
            if downloaded_files:
                st.success("Files downloaded successfully!")
                for file_path in downloaded_files:
                    file_name = os.path.basename(file_path)
                    with open(file_path, "rb") as file:
                        st.download_button(
                            label=f"Download {file_name}",
                            data=file,
                            file_name=file_name,
                            mime="audio/mpeg"
                        )
            else:
                st.warning("No files were downloaded. Please check the URLs and try again.")

if __name__ == "__main__":
    main()
