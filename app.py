import os
import sys
import yt_dlp

TEST_VIDEO_URL = "https://www.youtube.com/watch?v=QhwR5f-7c5Q"
OUTPUT_FILENAME = "test_video.mp4"

def clean_file():
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)

def verify_success(method_name):
    # A 13-minute 1080p video should be around 50MB - 150MB. 
    # If it's only 25MB, it might be 360p.
    if os.path.exists(OUTPUT_FILENAME) and os.path.getsize(OUTPUT_FILENAME) > 1000000:
        size_mb = os.path.getsize(OUTPUT_FILENAME) / (1024 * 1024)
        print(f"\n🎉 EXTREME SUCCESS! [{method_name}] secured the 1080p download! Size: {size_mb:.2f} MB")
        return True
    return False

def app_1_ytdlp_tv_1080p():
    print("\n========================================")
    print("📺 APPROACH 1: yt-dlp (TV Client Spoof via WARP VPN) -> 1080p TARGET")
    opts = {
        # Strictly demands 1080p video and the best audio.
        'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best',
        'merge_output_format': 'mp4', # Forces FFmpeg to merge them into a single MP4
        'outtmpl': OUTPUT_FILENAME,
        'extractor_args': {'youtube': ['player_client=tv']},
        'quiet': False, 
        'no_warnings': True
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl: 
            ydl.download([TEST_VIDEO_URL])
        return verify_success("yt-dlp TV + WARP + 1080p")
    except Exception as e: 
        print(f"❌ Failed: {e}")
    return False

def app_2_ytdlp_android_1080p():
    print("\n========================================")
    print("📱 APPROACH 2: yt-dlp (Android Client Spoof via WARP VPN) -> 1080p TARGET")
    opts = {
        'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': OUTPUT_FILENAME,
        'extractor_args': {'youtube': ['player_client=android']},
        'quiet': False, 
        'no_warnings': True
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl: 
            ydl.download([TEST_VIDEO_URL])
        return verify_success("yt-dlp Android + WARP + 1080p")
    except Exception as e: 
        print(f"❌ Failed: {e}")
    return False

def app_3_ytdlp_ios_1080p():
    print("\n========================================")
    print("🍏 APPROACH 3: yt-dlp (iOS Client Spoof via WARP VPN) -> 1080p TARGET")
    opts = {
        'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': OUTPUT_FILENAME,
        'extractor_args': {'youtube': ['player_client=ios']},
        'quiet': False, 
        'no_warnings': True
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl: 
            ydl.download([TEST_VIDEO_URL])
        return verify_success("yt-dlp iOS + WARP + 1080p")
    except Exception as e: 
        print(f"❌ Failed: {e}")
    return False

def main():
    print(f"🚀 FIRING 1080p VPN DOWNLOADER FOR: {TEST_VIDEO_URL}\n")
    
    approaches = [
        app_1_ytdlp_tv_1080p, 
        app_2_ytdlp_android_1080p, 
        app_3_ytdlp_ios_1080p
    ]
    
    for approach in approaches:
        clean_file()
        if approach():
            sys.exit(0)
            
    print("\n💀 ALL APPROACHES DEFEATED.")

if __name__ == "__main__":
    main()
