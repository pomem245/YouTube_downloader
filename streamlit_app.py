import streamlit as st
import os
import yt_dlp
from concurrent.futures import ThreadPoolExecutor

class YouTubeDownloader:
    def __init__(self):
        self.save_path = "downloads"
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        
    def download_url(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(self.save_path, '%(title)s.%(ext)s'),
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if 'entries' in info:  # It's a playlist
                    return [os.path.join(self.save_path, f"{entry['title']}.mp3") for entry in info['entries']]
                else:  # It's a single video
                    return [os.path.join(self.save_path, f"{info['title']}.mp3")]
        except Exception as e:
            st.error(f"Error downloading {url}: {str(e)}")
            return []

def main():
    st.title("YouTube MP3 Downloader")

    downloader = YouTubeDownloader()

    urls = st.text_area("Enter YouTube URL(s) (one per line, can include playlists):", placeholder="Enter URLs here...")
    
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
                    files = future.result()
                    downloaded_files.extend(files)
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
