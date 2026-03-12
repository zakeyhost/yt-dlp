import os
import sys
import yt_dlp
from pytubefix import YouTube

TEST_VIDEO_URL = "https://www.youtube.com/watch?v=QhwR5f-7c5Q"
OUTPUT_FILENAME = "test_video.mp4"
YOUTUBE_COOKIES_PATH = "cookies_yt.txt"

def clean_file():
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)

def verify_success(method_name):
    if os.path.exists(OUTPUT_FILENAME) and os.path.getsize(OUTPUT_FILENAME) > 1000000: # Ensure it's larger than 1MB
        size_mb = os.path.getsize(OUTPUT_FILENAME) / (1024 * 1024)
        print(f"\n🎉 EXTREME SUCCESS! [{method_name}] bypassed all blocks! Size: {size_mb:.2f} MB")
        return True
    return False

def app_1_ytdlp_vanilla():
    print("\n========================================")
    print("🚀 APPROACH 1: yt-dlp (Standard Engine via WARP VPN)")
    opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': OUTPUT_FILENAME,
        'quiet': False, 
        'no_warnings': True
    }
    if os.path.exists(YOUTUBE_COOKIES_PATH):
        print("🍪 Injecting YouTube Cookies...")
        opts['cookiefile'] = YOUTUBE_COOKIES_PATH
        
    try:
        with yt_dlp.YoutubeDL(opts) as ydl: 
            ydl.download([TEST_VIDEO_URL])
        return verify_success("yt-dlp Vanilla + WARP")
    except Exception as e: 
        print(f"❌ Failed: {e}")
    return False

def app_2_ytdlp_ios():
    print("\n========================================")
    print("📱 APPROACH 2: yt-dlp (iOS Client Spoof via WARP VPN)")
    opts = {
        'format': 'best',
        'outtmpl': OUTPUT_FILENAME,
        'extractor_args': {'youtube': ['player_client=ios']},
        'quiet': False, 
        'no_warnings': True
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl: 
            ydl.download([TEST_VIDEO_URL])
        return verify_success("yt-dlp iOS + WARP")
    except Exception as e: 
        print(f"❌ Failed: {e}")
    return False

def app_3_pytubefix_tv():
    print("\n========================================")
    print("📺 APPROACH 3: pytubefix (TV Client Spoof via WARP VPN)")
    try:
        yt = YouTube(TEST_VIDEO_URL, client='TV')
        stream = yt.streams.get_highest_resolution()
        stream.download(filename=OUTPUT_FILENAME)
        return verify_success("pytubefix TV + WARP")
    except Exception as e: 
        print(f"❌ Failed: {e}")
    return False

def main():
    print(f"🚀 FIRING VPN-SHIELDED DOWNLOADER FOR: {TEST_VIDEO_URL}\n")
    
    approaches = [
        app_1_ytdlp_vanilla, 
        app_2_ytdlp_ios, 
        app_3_pytubefix_tv
    ]
    
    for approach in approaches:
        clean_file()
        if approach():
            sys.exit(0)
            
    print("\n💀 ALL VPN APPROACHES DEFEATED. YouTube has blacklisted the WARP network.")

if __name__ == "__main__":
    main()
