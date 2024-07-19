import streamlit as st
import yt_dlp

def download_audio(link):
    ydl_opts = {
        'ignoreerrors': True,
        'extract_audio': True,
        'format': 'bestaudio',
        'outtmpl': '%(title)s.mp3'
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=True)
        
        if info_dict:
            video_title = info_dict.get('title', 'Unknown Title')
            st.write(f"Successfully downloaded: {video_title}")
            with open(f"{video_title}.mp3", "rb") as file:
                audio_data = file.read()
                st.download_button("Download Audio", audio_data, file_name=f"{video_title}.mp3", mime="audio/mpeg")
        else:
            st.write("There was an error downloading the audio.")

def main():
    st.title("YouTube Audio Downloader")
    url = st.text_input("Enter the YouTube link here:")
    if st.button("Download Audio"):
        download_audio(url)

if __name__ == "__main__":
    main()
