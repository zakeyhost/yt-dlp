import os
import sys
import time
import requests
from curl_cffi import requests as cffi_requests
import yt_dlp
from pytube import YouTube as LegacyYouTube
from pytubefix import YouTube as FixYouTube
from pytubefix.cli import on_progress

TEST_VIDEO_URL = "https://www.youtube.com/watch?v=QhwR5f-7c5Q"
OUTPUT_FILENAME = "test_video.mp4"
YOUTUBE_COOKIES_PATH = "cookies_yt.txt"

def verify_success(method_name):
    if os.path.exists(OUTPUT_FILENAME) and os.path.getsize(OUTPUT_FILENAME) > 1000000:
        size_mb = os.path.getsize(OUTPUT_FILENAME) / (1024 * 1024)
        print(f"\n🎉 SUCCESS! [{method_name}] downloaded the video! Size: {size_mb:.2f} MB")
        return True
    return False

def clean_file():
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)

# =====================================================================
# 1. IMPLEMENTING: pedrohusky/youtube-python-downloader & divyanshupatel17
# Core Engine: Legacy pytube
# =====================================================================
def repo_legacy_pytube():
    print("\n" + "="*60)
    print("▶️ REPO TEST: pedrohusky & divyanshupatel17 (Legacy pytube)")
    try:
        yt = LegacyYouTube(TEST_VIDEO_URL)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        stream.download(filename=OUTPUT_FILENAME)
        return verify_success("Legacy pytube")
    except Exception as e: print(f"❌ Failed: {e}")
    return False

# =====================================================================
# 2. IMPLEMENTING: zararashraf/youtube-video-downloader-api & Cangregito
# Core Engine: pytubefix (Vanilla + TV Spoofing)
# =====================================================================
def repo_pytubefix_vanilla():
    print("\n" + "="*60)
    print("▶️ REPO TEST: zararashraf & Cangregito (pytubefix - Web/TV Client)")
    try:
        # Cangregito specifically uses client='TV' to bypass some blocks
        yt = FixYouTube(TEST_VIDEO_URL, client='TV', on_progress_callback=on_progress)
        stream = yt.streams.get_highest_resolution()
        stream.download(filename=OUTPUT_FILENAME)
        return verify_success("pytubefix TV Client")
    except Exception as e: print(f"❌ Failed: {e}")
    return False

# =====================================================================
# 3. IMPLEMENTING: Ukiyo-AK, Rigor-Core, nubsuki, epsill0n
# Core Engine: yt-dlp (Vanilla UI Wrappers)
# =====================================================================
def repo_ytdlp_vanilla():
    print("\n" + "="*60)
    print("▶️ REPO TEST: Ukiyo-AK, Rigor-Core, nubsuki, epsill0n (yt-dlp)")
    opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': OUTPUT_FILENAME,
        'quiet': True, 'no_warnings': True
    }
    # Included from Rigor-Core's cookie implementation
    if os.path.exists(YOUTUBE_COOKIES_PATH): opts['cookiefile'] = YOUTUBE_COOKIES_PATH
    try:
        with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([TEST_VIDEO_URL])
        return verify_success("yt-dlp Vanilla")
    except Exception as e: print(f"❌ Failed: {str(e).split(';')[0][:100]}...")
    return False

# =====================================================================
# 4. IMPLEMENTING: Simatwa/youtube-downloader-api 
# Core Engine: yt-dlp + PO Token Provider Plugin
# =====================================================================
def repo_simatwa_potoken():
    print("\n" + "="*60)
    print("▶️ REPO TEST: Simatwa (yt-dlp + PO Token Plugin from Wiki)")
    opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': OUTPUT_FILENAME,
        'quiet': True, 'no_warnings': True
    }
    try:
        # The bgutil-ytdlp-pot-provider plugin intercepts this automatically if installed
        with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([TEST_VIDEO_URL])
        return verify_success("yt-dlp + PO Token Plugin")
    except Exception as e: print(f"❌ Failed: {str(e).split(';')[0][:100]}...")
    return False

# =====================================================================
# 5. FALLBACK: The Tor Network (Dark Web Bypass)
# =====================================================================
def fallback_tor_ytdlp():
    print("\n" + "="*60)
    print("▶️ FALLBACK: yt-dlp via Tor Network (Bypass Datacenter IP Ban)")
    opts = {
        'format': 'best', 'outtmpl': OUTPUT_FILENAME,
        'proxy': 'socks5://127.0.0.1:9050',
        'quiet': True, 'no_warnings': True, 'socket_timeout': 30
    }
    for attempt in range(1, 4):
        try:
            with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([TEST_VIDEO_URL])
            if verify_success("Tor Network"): return True
        except:
            print(f"   -> Tor node blocked, rotating IP...")
            os.system("sudo systemctl restart tor")
            time.sleep(5)
    return False

# =====================================================================
# 6. FALLBACK: YT5S with curl_cffi (Cloudflare TLS Bypass)
# =====================================================================
def fallback_yt5s_cffi():
    print("\n" + "="*60)
    print("▶️ FALLBACK: YT5S Backend via curl_cffi")
    try:
        headers = {"Origin": "https://yt5s.biz", "Referer": "https://yt5s.biz/en117/"}
        data = {"q": TEST_VIDEO_URL, "vt": "home"}
        res = cffi_requests.post("https://yt5s.biz/api/ajaxSearch/index", data=data, headers=headers, impersonate="chrome120", timeout=15).json()
        
        vid = res.get("vid")
        best_k = list(res.get("links", {}).get("mp4", {}).values())[0].get("k")
        if not best_k: return False
        
        for _ in range(5): 
            c_res = cffi_requests.post("https://yt5s.biz/api/ajaxConvert/convert", data={"vid": vid, "k": best_k}, headers=headers, impersonate="chrome120", timeout=15).json()
            if c_res.get("dlink"):
                with cffi_requests.get(c_res["dlink"], stream=True, impersonate="chrome120", timeout=60) as r:
                    with open(OUTPUT_FILENAME, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
                return verify_success("YT5S + curl_cffi")
            time.sleep(3)
    except Exception as e: print(f"❌ Failed: {e}")
    return False

def main():
    print(f"🚀 FIRING COMPREHENSIVE REPO TEST FOR: {TEST_VIDEO_URL}\n")
    
    approaches = [
        repo_legacy_pytube,
        repo_pytubefix_vanilla,
        repo_ytdlp_vanilla,
        repo_simatwa_potoken,
        fallback_tor_ytdlp,
        fallback_yt5s_cffi
    ]
    
    for approach in approaches:
        clean_file()
        if approach():
            sys.exit(0)
            
    print("\n💀 ALL IMPLEMENTATIONS BLOCKED BY YOUTUBE/CLOUDFLARE.")

if __name__ == "__main__":
    main()
