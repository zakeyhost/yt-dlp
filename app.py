import os
import sys
import requests
import time
import yt_dlp

TEST_VIDEO_URL = "https://www.youtube.com/watch?v=QhwR5f-7c5Q"
OUTPUT_FILENAME = "test_video.mp4"

def download_file(url, filename):
    print(f"⬇️ Streaming MP4 directly to GitHub Runner...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        with requests.get(url, stream=True, headers=headers, timeout=60) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        if os.path.exists(filename) and os.path.getsize(filename) > 1024:
            file_size_mb = os.path.getsize(filename) / (1024 * 1024)
            print(f"✅ SUCCESS! Video secured. Size: {file_size_mb:.2f} MB")
            return True
    except Exception as e:
        print(f"❌ Direct stream failed: {e}")
    return False

def approach_1_yt5s_backend():
    print("\n" + "="*50)
    print("🚀 APPROACH 1: YT5S Backend API (AJAX Bypass)")
    print("="*50)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://yt5s.biz",
            "Referer": "https://yt5s.biz/en117/"
        }
        
        print("🔍 Step 1: Sending hidden backend search request...")
        data = {"q": TEST_VIDEO_URL, "vt": "home"}
        res = requests.post("https://yt5s.biz/api/ajaxSearch/index", data=data, headers=headers, timeout=15)
        j = res.json()
        
        vid = j.get("vid")
        links = j.get("links", {}).get("mp4", {})
        
        if not links:
            print("❌ YT5S could not generate mp4 links.")
            return False
            
        print("⚙️ Step 2: Parsing video qualities...")
        best_k = None
        for q in ["1080p", "720p", "480p", "auto"]:
            for key, val in links.items():
                if val.get("q") == q:
                    best_k = val.get("k")
                    print(f"🎯 Target quality locked: {q}")
                    break
            if best_k: break
            
        if not best_k:
            best_k = list(links.values())[0].get("k")
            
        print("⏳ Step 3: Forcing server-side conversion...")
        conv_data = {"vid": vid, "k": best_k}
        
        # Poll the server until the file is ready
        for _ in range(10): 
            conv_res = requests.post("https://yt5s.biz/api/ajaxConvert/convert", data=conv_data, headers=headers, timeout=15)
            c_j = conv_res.json()
            
            if c_j.get("c_status") == "CONVERTING":
                print("...Server is converting video... waiting 3 seconds...")
                time.sleep(3)
                continue
                
            dlink = c_j.get("dlink")
            if dlink:
                print("🔗 BINGO! Extracted RAW MP4 Link from backend!")
                return download_file(dlink, OUTPUT_FILENAME)
            else:
                print("❌ Conversion failed or timed out on server.")
                break
                
    except Exception as e:
        print(f"❌ YT5S Backend Error: {e}")
    return False

def approach_2_yt1s_backend():
    print("\n" + "="*50)
    print("🚀 APPROACH 2: YT1S Backend API (AJAX Bypass)")
    print("="*50)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://yt1s.com",
            "Referer": "https://yt1s.com/en361"
        }
        
        print("🔍 Step 1: Sending hidden backend search request...")
        data = {"q": TEST_VIDEO_URL, "vt": "home"}
        res = requests.post("https://yt1s.com/api/ajaxSearch/index", data=data, headers=headers, timeout=15)
        j = res.json()
        
        vid = j.get("vid")
        links = j.get("links", {}).get("mp4", {})
        
        if not links:
            print("❌ YT1S could not generate mp4 links.")
            return False
            
        print("⚙️ Step 2: Parsing video qualities...")
        best_k = None
        for q in ["1080p", "720p", "480p", "auto"]:
            for key, val in links.items():
                if val.get("q") == q:
                    best_k = val.get("k")
                    print(f"🎯 Target quality locked: {q}")
                    break
            if best_k: break
            
        if not best_k:
            best_k = list(links.values())[0].get("k")
            
        print("⏳ Step 3: Forcing server-side conversion...")
        conv_data = {"vid": vid, "k": best_k}
        
        for _ in range(10): 
            conv_res = requests.post("https://yt1s.com/api/ajaxConvert/convert", data=conv_data, headers=headers, timeout=15)
            c_j = conv_res.json()
            
            if c_j.get("c_status") == "CONVERTING":
                print("...Server is converting video... waiting 3 seconds...")
                time.sleep(3)
                continue
                
            dlink = c_j.get("dlink")
            if dlink:
                print("🔗 BINGO! Extracted RAW MP4 Link from backend!")
                return download_file(dlink, OUTPUT_FILENAME)
            else:
                print("❌ Conversion failed or timed out on server.")
                break
                
    except Exception as e:
        print(f"❌ YT1S Backend Error: {e}")
    return False

def approach_3_ytdlp_ios_spoof():
    print("\n" + "="*50)
    print("⚔️ APPROACH 3: yt-dlp (iOS Client Spoofing - NO COOKIES)")
    print("="*50)
    # Sometimes cookies flag the account. This approach strips cookies entirely 
    # and forces YouTube to treat the scraper like an old iPhone app, which has lighter bot-checks.
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': OUTPUT_FILENAME,
        'merge_output_format': 'mp4',
        'extractor_args': {'youtube': ['player_client=ios,web']},
        'quiet': False,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([TEST_VIDEO_URL])
            
        if os.path.exists(OUTPUT_FILENAME) and os.path.getsize(OUTPUT_FILENAME) > 1024:
            file_size_mb = os.path.getsize(OUTPUT_FILENAME) / (1024 * 1024)
            print(f"✅ SUCCESS! yt-dlp iOS spoof bypassed the bot-check! Size: {file_size_mb:.2f} MB")
            return True
    except Exception as e:
        print(f"❌ yt-dlp iOS spoof failed: {e}")
        
    return False

def main():
    print(f"🚀 Starting DIRECT BACKEND AJAX test for: {TEST_VIDEO_URL}\n")
    
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)
        
    if approach_1_yt5s_backend():
        sys.exit(0)
        
    if approach_2_yt1s_backend():
        sys.exit(0)
        
    if approach_3_ytdlp_ios_spoof():
        sys.exit(0)
        
    print("\n💀 ALL BACKEND APPROACHES FAILED.")

if __name__ == "__main__":
    main()
