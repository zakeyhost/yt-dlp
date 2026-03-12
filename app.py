import os
import yt_dlp

# Configurations
YOUTUBE_COOKIES_PATH = "cookies_yt.txt"
TEST_VIDEO_URL = "https://www.youtube.com/watch?v=QhwR5f-7c5Q"
OUTPUT_FILENAME = "test_video.mp4"

def main():
    print(f"🚀 Starting yt-dlp test for video: {TEST_VIDEO_URL}")
    
    # 1. CONFIGURE YT-DLP
    # This format asks for the best mp4 video + m4a audio, merging them.
    # If that exact combo isn't available, it falls back to the best single file.
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': OUTPUT_FILENAME,
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': False
    }

    # Inject cookies if the file exists
    if os.path.exists(YOUTUBE_COOKIES_PATH):
        print("🍪 Found cookies_yt.txt! Injecting to bypass age/region restrictions...")
        ydl_opts['cookiefile'] = YOUTUBE_COOKIES_PATH
    else:
        print("⚠️ WARNING: cookies_yt.txt not found. Attempting guest download...")

    # 2. DOWNLOAD VIDEO
    print("⬇️ Downloading video using yt-dlp...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([TEST_VIDEO_URL])
        print("✅ Download command completed without crashing!")
    except Exception as e:
        print(f"❌ yt-dlp Failed to download the video. Error: {e}")
        return

    # 3. VERIFY THE FILE
    if not os.path.exists(OUTPUT_FILENAME):
        print("❌ ERROR: Download script finished, but test_video.mp4 is missing from the directory.")
        return

    file_size_mb = os.path.getsize(OUTPUT_FILENAME) / (1024 * 1024)
    print(f"✅ SUCCESS! The video was downloaded successfully.")
    print(f"📊 Final File size: {file_size_mb:.2f} MB")
    print("GitHub Actions will now upload this file as an artifact so you can download it.")

if __name__ == "__main__":
    main()
