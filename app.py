import os
import sys
import requests
import yt_dlp

TEST_VIDEO_URL = "https://www.youtube.com/watch?v=QhwR5f-7c5Q"
VIDEO_ID = "QhwR5f-7c5Q"
OUTPUT_FILENAME = "test_video.mp4"
YOUTUBE_COOKIES_PATH = "cookies_yt.txt"

def download_file(url, filename):
    print("⬇️ Streaming MP4 directly to GitHub Runner...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        file_size_mb = os.path.getsize(filename) / (1024 * 1024)
        print(f"✅ SUCCESS! Video secured. Size: {file_size_mb:.2f} MB")
        return True
    return False

def approach_1_cobalt():
    print("\n" + "="*50)
    print("👻 APPROACH 1: Cobalt API (Off-Server Proxy)")
    print("="*50)
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {"url": TEST_VIDEO_URL, "vQuality": "1080"}
    
    # List of public Cobalt instances to try
    instances = ["https://api.cobalt.tools", "https://cobalt-api.kwiateks.com", "https://co.wuk.sh"]
    
    for instance in instances:
        print(f"🔌 Connecting to Cobalt instance: {instance}...")
        try:
            res = requests.post(f"{instance}/api/json" if "tools" in instance else instance, json=payload, headers=headers, timeout=15)
            if res.status_code == 200:
                data = res.json()
                if 'url' in data:
                    print("✅ Cobalt successfully bypassed YouTube! Extracted raw MP4 link.")
                    return download_file(data['url'], OUTPUT_FILENAME)
            else:
                print(f"⚠️ Instance failed with status: {res.status_code}")
        except Exception as e:
            print(f"⚠️ Instance unreachable: {e}")
            
    print("❌ All Cobalt instances blocked or overloaded.")
    return False

def approach_2_invidious():
    print("\n" + "="*50)
    print("🕵️ APPROACH 2: Invidious API (Ghost Network)")
    print("="*50)
    
    instances = ["https://invidious.perennialte.ch", "https://iv.melmac.space"]
    
    for instance in instances:
        print(f"🔌 Connecting to Invidious instance: {instance}...")
        try:
            res = requests.get(f"{instance}/api/v1/videos/{VIDEO_ID}", timeout=15)
            if res.status_code == 200:
                data = res.json()
                streams = data.get('formatStreams', [])
                if streams:
                    best_stream = streams[-1] # Usually 720p/1080p MP4
                    url = best_stream.get('url')
                    print("✅ Invidious successfully extracted the link!")
                    return download_file(url, OUTPUT_FILENAME)
        except Exception as e:
            print(f"⚠️ Instance failed: {e}")
            
    print("❌ Invidious extraction failed.")
    return False

def approach_3_nightly_yt_dlp():
    print("\n" + "="*50)
    print("⚔️ APPROACH 3: Bleeding-Edge Nightly yt-dlp + Cookies")
    print("="*50)
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': OUTPUT_FILENAME,
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': True,
    }
    
    if os.path.exists(YOUTUBE_COOKIES_PATH):
        print("🍪 Injecting cookies_yt.txt...")
        ydl_opts['cookiefile'] = YOUTUBE_COOKIES_PATH
        
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([TEST_VIDEO_URL])
            
        if os.path.exists(OUTPUT_FILENAME) and os.path.getsize(OUTPUT_FILENAME) > 0:
            file_size_mb = os.path.getsize(OUTPUT_FILENAME) / (1024 * 1024)
            print(f"✅ SUCCESS! Nightly yt-dlp bypassed the bot-check! Size: {file_size_mb:.2f} MB")
            return True
    except Exception as e:
        print(f"❌ yt-dlp failed: {e}")
        
    return False

def main():
    print(f"🚀 Starting GHOST DOWNLOADER test for: {TEST_VIDEO_URL}\n")
    
    if approach_1_cobalt():
        sys.exit(0)
        
    if approach_2_invidious():
        sys.exit(0)
        
    if approach_3_nightly_yt_dlp():
        sys.exit(0)
        
    print("\n💀 ALL APPROACHES FAILED. YouTube's Datacenter IP ban is impenetrable on this video.")

if __name__ == "__main__":
    main()
