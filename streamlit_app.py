import requests
from bs4 import BeautifulSoup
import subprocess
import os

def get_video_info(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the page: {url}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find("title").text
    return title

def download_video(url, output_path):
    result = subprocess.run([
        'youtube-dl',
        '-f', 'bestaudio/best',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--output', os.path.join(output_path, '%(title)s.%(ext)s'),
        url
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"youtube-dl failed: {result.stderr}")
    print(result.stdout)

if __name__ == "__main__":
    video_url = input("Enter the URL of the YouTube video: ")
    save_path = input("Enter the path where the MP3 should be saved (leave blank for current directory): ")
    if save_path.strip() == "":
        save_path = "."

    title = get_video_info(video_url)
    print(f"Video title: {title}")
    
    download_video(video_url, save_path)
    print(f"Downloaded and converted {title} to MP3 successfully!")
