import yt_dlp
import streamlit as st

def download_audio(link):
    ydl_opts = {
        'ignoreerrors': True,
        'extract_audio': True,
        'format': 'bestaudio',
        'outtmpl': '%(title)s.%(ext)s'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=True)
        
        if info_dict:
            video_title = info_dict.get('title', 'Unknown Title')
            filename = f"{video_title}.mp3"
            return filename, video_title
        else:
            return None, None

st.title("YouTube Audio Downloader")

url = st.text_input("Paste YouTube link here:")
if st.button("Download"):
    if url:
        with st.spinner("Downloading..."):
            filename, video_title = download_audio(url)
            
            if filename:
                with open(filename, 'rb') as f:
                    audio_data = f.read()
                st.success(f"Successfully downloaded: {video_title}")
                st.download_button(
                    label="Download Audio",
                    data=audio_data,
                    file_name=filename,
                    mime="audio/mpeg",
                )
            else:
                st.error("There was an error downloading the audio.")
    else:
        st.warning("Please enter a valid YouTube link.")
