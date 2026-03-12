import os
import sys
import time
import random
import requests
import asyncio
import yt_dlp
from pytubefix import YouTube as PyTubeFixYT
from pytube import YouTube as LegacyPyTubeYT
from playwright.async_api import async_playwright

TEST_VIDEO_URL = "https://www.youtube.com/watch?v=QhwR5f-7c5Q"
OUTPUT_FILENAME = "test_video.mp4"
YOUTUBE_COOKIES_PATH = "cookies_yt.txt"

def verify_success(method_name):
    """Checks if the file exists and has actual content."""
    if os.path.exists(OUTPUT_FILENAME) and os.path.getsize(OUTPUT_FILENAME) > 500000: # Larger than 500KB
        size_mb = os.path.getsize(OUTPUT_FILENAME) / (1024 * 1024)
        print(f"\n🎉 EXTREME SUCCESS! [{method_name}] bypassed YouTube's defenses! Size: {size_mb:.2f} MB")
        return True
    return False

def clean_file():
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)

def stream_download(url, filename, headers=None):
    if not headers:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        with requests.get(url, stream=True, headers=headers, timeout=60) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
        return True
    except: return False

# ==========================================
# GITHUB REPO IMPLEMENTATIONS (PYTUBE & PYTUBEFIX)
# ==========================================

def app_1_pytubefix_tv_client():
    print("\n⚔️ 1. Pytubefix (Spoofing TV Client - Bypasses PO Token)")
    try:
        yt = PyTubeFixYT(TEST_VIDEO_URL, client='TV')
        stream = yt.streams.get_highest_resolution()
        stream.download(filename=OUTPUT_FILENAME)
        return verify_success("Pytubefix TV Client")
    except Exception as e: print(f"❌ Failed: {e}")
    return False

def app_2_pytubefix_android_vr():
    print("\n⚔️ 2. Pytubefix (Spoofing Android VR Client)")
    try:
        yt = PyTubeFixYT(TEST_VIDEO_URL, client='ANDROID_VR')
        stream = yt.streams.get_highest_resolution()
        stream.download(filename=OUTPUT_FILENAME)
        return verify_success("Pytubefix Android VR")
    except Exception as e: print(f"❌ Failed: {e}")
    return False

def app_3_pytubefix_oauth():
    print("\n⚔️ 3. Pytubefix (OAuth Mode)")
    try:
        yt = PyTubeFixYT(TEST_VIDEO_URL, use_oauth=True, allow_oauth_cache=True)
        stream = yt.streams.get_highest_resolution()
        stream.download(filename=OUTPUT_FILENAME)
        return verify_success("Pytubefix OAuth")
    except Exception as e: print(f"❌ Failed (Expected without human interaction): {e}")
    return False

def app_4_legacy_pytube():
    print("\n⚔️ 4. Legacy Pytube (From divyanshupatel17 Repo)")
    try:
        yt = LegacyPyTubeYT(TEST_VIDEO_URL)
        stream = yt.streams.get_highest_resolution()
        stream.download(filename=OUTPUT_FILENAME)
        return verify_success("Legacy Pytube")
    except Exception as e: print(f"❌ Failed: {e}")
    return False

# ==========================================
# YT-DLP + WIKI PO TOKEN PLUGIN IMPLEMENTATIONS
# ==========================================

def app_5_ytdlp_potoken_plugin():
    print("\n⚔️ 5. yt-dlp + bgutil PO Token Provider Plugin (Wiki Recommended)")
    opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': OUTPUT_FILENAME,
        'quiet': True, 'no_warnings': True
    }
    if os.path.exists(YOUTUBE_COOKIES_PATH): opts['cookiefile'] = YOUTUBE_COOKIES_PATH
    try:
        with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([TEST_VIDEO_URL])
        return verify_success("yt-dlp + PO Token Plugin")
    except Exception as e: print(f"❌ Failed: {str(e)[:100]}")
    return False

def app_6_ytdlp_ios_client():
    print("\n⚔️ 6. yt-dlp (Spoofing iOS Client without cookies)")
    opts = {
        'format': 'best', 'outtmpl': OUTPUT_FILENAME,
        'extractor_args': {'youtube': ['player_client=ios']},
        'quiet': True, 'no_warnings': True
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([TEST_VIDEO_URL])
        return verify_success("yt-dlp iOS Client")
    except Exception as e: print(f"❌ Failed: {str(e)[:100]}")
    return False

# ==========================================
# PUBLIC PROXY POOL (IP MASKING)
# ==========================================

def app_7_ytdlp_free_proxy():
    print("\n⚔️ 7. yt-dlp + Scraped Free Proxy (IP Masking)")
    try:
        r = requests.get("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt", timeout=10)
        proxies = r.text.strip().split('\n')
        random.shuffle(proxies)
        for proxy in proxies[:3]: # Try 3 random proxies
            print(f"   -> Testing proxy: {proxy}")
            opts = {
                'format': 'best', 'outtmpl': OUTPUT_FILENAME,
                'proxy': f"http://{proxy.strip()}", 'socket_timeout': 10,
                'quiet': True, 'no_warnings': True
            }
            try:
                with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([TEST_VIDEO_URL])
                if verify_success(f"yt-dlp via Proxy {proxy}"): return True
            except: pass
    except: print("❌ Failed to fetch or use proxies.")
    return False

# ==========================================
# 3RD PARTY API & BACKEND AJAX SCRAPERS
# ==========================================

def app_8_loader_to_api():
    print("\n⚔️ 8. Loader.to AJAX API")
    try:
        task = requests.get(f"https://p.loader.to/ajax/download.php?format=1080&url={TEST_VIDEO_URL}", timeout=10).json()
        for _ in range(12): # Poll for 1 minute
            time.sleep(5)
            prog = requests.get(f"https://p.loader.to/ajax/progress.php?id={task['id']}", timeout=10).json()
            if prog.get("download_url"):
                stream_download(prog["download_url"], OUTPUT_FILENAME)
                return verify_success("Loader.to API")
    except Exception as e: print(f"❌ Failed: {e}")
    return False

def app_9_cobalt_tracker():
    print("\n⚔️ 9. Cobalt Public Tracker Instances")
    try:
        instances = requests.get("https://instances.cobalt.tools/api/instances", timeout=10).json()
        active = [i["domain"] for i in instances if i.get("api_online")]
        random.shuffle(active)
        for domain in active[:3]:
            url = f"https://{domain}/api/json" if not domain.startswith("http") else f"{domain}/api/json"
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            try:
                r = requests.post(url, json={"url": TEST_VIDEO_URL}, headers=headers, timeout=10)
                if r.status_code == 200 and 'url' in r.json():
                    stream_download(r.json()['url'], OUTPUT_FILENAME)
                    return verify_success("Cobalt Tracker API")
            except: pass
    except Exception as e: print(f"❌ Failed: {e}")
    return False

def app_10_yt5s_backend():
    print("\n⚔️ 10. YT5S Backend AJAX")
    headers = {"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest"}
    try:
        r1 = requests.post("https://yt5s.biz/api/ajaxSearch/index", data={"q": TEST_VIDEO_URL, "vt": "home"}, headers=headers, timeout=10).json()
        k = list(r1['links']['mp4'].values())[0]['k']
        for _ in range(5):
            r2 = requests.post("https://yt5s.biz/api/ajaxConvert/convert", data={"vid": r1['vid'], "k": k}, headers=headers, timeout=10).json()
            if r2.get("dlink"):
                stream_download(r2["dlink"], OUTPUT_FILENAME)
                return verify_success("YT5S Backend")
            time.sleep(3)
    except Exception as e: print(f"❌ Failed: {e}")
    return False

# ==========================================
# PLAYWRIGHT STEALTH WEB SCRAPERS
# ==========================================

async def app_11_downr_playwright():
    print("\n⚔️ 11. downr.org (Playwright Stealth)")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        page = await browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        try:
            await page.goto("https://downr.org/", timeout=30000)
            await page.get_by_placeholder("Paste URL here").fill(TEST_VIDEO_URL)
            await page.locator('button', has_text="Download").first.click()
            await page.wait_for_selector('text="mp4 ("', timeout=30000)
            element = page.locator('a:has-text("mp4 (")').first
            url = await element.get_attribute("href")
            stream_download(url, OUTPUT_FILENAME, {"Referer": "https://downr.org/"})
            return verify_success("downr.org Scraper")
        except Exception as e: print(f"❌ Failed: {str(e)[:100]}")
        finally: await browser.close()
    return False

async def app_12_ssyoutube_playwright():
    print("\n⚔️ 12. SSYouTube (Playwright Stealth)")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto("https://ssyoutube.com/en731v/", timeout=30000)
            await page.fill('#id_url', TEST_VIDEO_URL)
            await page.click('#search')
            await page.wait_for_selector('a.download-icon', timeout=30000)
            url = await page.get_attribute('a.download-icon', 'href')
            stream_download(url, OUTPUT_FILENAME)
            return verify_success("SSYouTube Scraper")
        except Exception as e: print(f"❌ Failed: {str(e)[:100]}")
        finally: await browser.close()
    return False

def main():
    print(f"🚀 FIRING GOD-MODE DOWNLOADER FOR: {TEST_VIDEO_URL}\n")
    
    approaches = [
        app_1_pytubefix_tv_client,
        app_2_pytubefix_android_vr,
        app_5_ytdlp_potoken_plugin,
        app_6_ytdlp_ios_client,
        app_8_loader_to_api,
        app_9_cobalt_tracker,
        app_10_yt5s_backend,
        lambda: asyncio.run(app_11_downr_playwright()),
        lambda: asyncio.run(app_12_ssyoutube_playwright()),
        app_7_ytdlp_free_proxy,
        app_4_legacy_pytube,
        app_3_pytubefix_oauth
    ]

    for attempt, approach in enumerate(approaches, 1):
        clean_file()
        if approach():
            print("\n✅ MISSION ACCOMPLISHED. Exiting God-Mode.")
            sys.exit(0)
            
    print("\n💀 ALL 12 APPROACHES DESTROYED BY YOUTUBE. The Datacenter IP block is absolute.")

if __name__ == "__main__":
    main()
