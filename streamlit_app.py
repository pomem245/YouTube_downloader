import streamlit as st
import re
from pytube import YouTube, Playlist
import io

class YouTubeDownloader:
    def __init__(self):
        pass
        
    def download_url(self, url):
        try:
            if 'playlist' in url:
                playlist = Playlist(url)
                for video in playlist.videos:
                    yield self.download_video(video)
            else:
                video = YouTube(url)
                yield self.download_video(video)
        except Exception as e:
            st.error(f"Error with URL {url}: {e}")

    def download_video(self, video):
        try:
            stream = video.streams.filter(only_audio=True).first()
            buffer = io.BytesIO()
            stream.stream_to_buffer(buffer)
            buffer.seek(0)
            sanitized_title = self.sanitize_filename(video.title)
            return sanitized_title, buffer.getvalue()
        except Exception as e:
            st.error(f"Error downloading video {video.title}: {e}")
            return None, None

    def sanitize_filename(self, filename):
        return re.sub(r'[<>:"/\\|?*]', '', filename)

@st.cache_data
def cached_download_video(video):
    downloader = YouTubeDownloader()
    return downloader.download_video(video)

def main():
    st.title("YouTube MP3 Downloader")

    urls = st.text_area("Enter YouTube URL(s) (one per line or playlist URL):", height=100)

    if st.button("Download MP3"):
        if not urls.strip():
            st.error("Please enter at least one YouTube URL")
            return

        url_list = [url.strip() for url in urls.strip().split('\n') if url.strip()]

        progress_bar = st.progress(0)
        status_text = st.empty()

        downloader = YouTubeDownloader()

        for i, url in enumerate(url_list):
            if 'playlist' in url:
                playlist = Playlist(url)
                for j, video in enumerate(playlist.videos):
                    title, audio_data = cached_download_video(video)
                    if title and audio_data:
                        st.download_button(
                            label=f"Download {title}.mp3",
                            data=audio_data,
                            file_name=f"{title}.mp3",
                            mime="audio/mpeg"
                        )
                    progress = int((i + (j+1)/len(playlist.videos)) / len(url_list) * 100)
                    progress_bar.progress(progress)
                    status_text.text(f"Downloading... {progress}%")
            else:
                video = YouTube(url)
                title, audio_data = cached_download_video(video)
                if title and audio_data:
                    st.download_button(
                        label=f"Download {title}.mp3",
                        data=audio_data,
                        file_name=f"{title}.mp3",
                        mime="audio/mpeg"
                    )
                progress = int((i + 1) / len(url_list) * 100)
                progress_bar.progress(progress)
                status_text.text(f"Downloading... {progress}%")

        st.success("Download complete")

if __name__ == "__main__":
    main()
