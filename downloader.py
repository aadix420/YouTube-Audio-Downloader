import os
import pytube
import requests
from tqdm import tqdm
from urllib.parse import urlparse
from colorama import Fore, Back, Style, init

# initialize colorama
init()

# function to download a single audio file
def download_audio(url):
    try:
        # create a YouTube object and get the audio stream
        yt = pytube.YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        # get the file name and extension based on user choice
        file_name = yt.title
        while True:
            audio_format = input(Fore.CYAN + "Enter audio format (mp3 or wav): ")
            if audio_format == 'mp3':
                file_ext = '.mp3'
                break
            elif audio_format == 'wav':
                file_ext = '.wav'
                break
            else:
                print(Fore.RED + "Invalid audio format. Please enter mp3 or wav.")
        file_name += file_ext

        # create the downloads directory if it does not exist
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        # download the audio stream and show the progress bar
        response = requests.get(audio_stream.url, stream=True)
        response.raise_for_status()
        filepath = os.path.join('downloads', file_name)
        with open(filepath, 'wb') as f:
            total_size = int(response.headers.get('content-length', 0))
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
            for data in response.iter_content(chunk_size=1024):
                progress_bar.update(len(data))
                f.write(data)
        print(Fore.GREEN + "Audio file saved as:", filepath)
    except (requests.exceptions.RequestException, pytube.exceptions.PytubeError) as e:
        print(Fore.RED + "Error downloading audio:", e)

# function to download all audio files from a playlist
def download_playlist(url):
    try:
        # create a YouTube playlist object
        playlist = pytube.Playlist(url)

        # loop through each video in the playlist and download its audio stream
        for video in playlist.videos:
            download_audio(video.watch_url)
    except pytube.exceptions.PytubeError as e:
        print(Fore.RED + "Error downloading playlist:", e)

# main program loop
while True:
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + "\n============================")
        print(Fore.CYAN + " YouTube Audio Downloader")
        print(Fore.CYAN + "============================")
        print(Fore.CYAN + "1. Download a single audio file")
        print(Fore.CYAN + "2. Download all audio files from a playlist")
        choice = input(Fore.CYAN + "Enter your choice (1 or 2): ")
        if choice == '1':
            while True:
                url = input(Fore.YELLOW + "Enter the YouTube video URL: ")
                if "youtube.com" in url.lower() and urlparse(url).scheme in ["http", "https"]:
                    break
                else:
                    print(Fore.RED + "Invalid YouTube URL. Please enter a valid YouTube URL.")
            download_audio(url)
            input("\nPress Enter to continue...")
        elif choice == '2':
            while True:
                url = input(Fore.YELLOW + "Enter the YouTube playlist URL: ")
                if "youtube.com" in url.lower() and urlparse(url).scheme in ["http", "https"]:
                    break
                else:
                    print(Fore.RED + "Invalid YouTube URL. Please enter a valid YouTube URL.")
            download_playlist(url)
            input("\nPress Enter to continue...")
        else:
            print(Fore.RED + "Invalid choice. Please enter '1' or '2'.")
            input("\nPress Enter to continue...")
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgram canceled by user.")
        break

print(Fore.GREEN + "\nThank you for using YouTube Audio Downloader! ^_^")
