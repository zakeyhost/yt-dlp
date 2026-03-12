import os
import sys
import time
import requests
from curl_cffi import requests as cffi_requests
import asyncio
from playwright.async_api import async_playwright

TEST_VIDEO_URL = "https://www.youtube.com/watch?v=QhwR5f-7c5Q"
TEST_VIDEO_ID = "QhwR5f-7c5Q"
OUTPUT_FILENAME = "test_video.mp4"

def clean_file():
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)

def verify_success(method_name):
    if os.path.exists(OUTPUT_FILENAME) and os.path.getsize(OUTPUT_FILENAME) > 500000:
        size_mb = os.path.getsize(OUTPUT_FILENAME) / (1024 * 1024)
        print(f"\n🎉 EXTREME SUCCESS! [{method_name}] bypassed all firewalls! Size: {size_mb:.2f} MB")
        return True
    return False

def stream_download(url, filename, headers=None):
    print("⬇️ Streaming MP4 directly to GitHub Runner...")
    if not headers:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        with cffi_requests.get(url, stream=True, headers=headers, impersonate="chrome120", timeout=60) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"❌ Direct stream failed: {e}")
    return False

# =====================================================================
# APPROACH 1: The Invidious Network (Decentralized YouTube)
# =====================================================================
def approach_1_invidious():
    print("\n" + "="*60)
    print("🌍 APPROACH 1: Invidious Decentralized API (Immune to Cloudflare)")
    try:
        instances = [
            "https://invidious.jing.rocks", 
            "https://vid.puffyan.us", 
            "https://invidious.nerdvpn.de",
            "https://invidious.perennialte.ch", 
            "https://yewtu.be"
        ]
        for instance in instances:
            print(f"   -> Pinging backend: {instance}...")
            try:
                res = requests.get(f"{instance}/api/v1/videos/{TEST_VIDEO_ID}", timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    formats = data.get("formatStreams", [])
                    if formats:
                        # Grab the best MP4 available
                        best_stream = [f for f in formats if 'mp4' in f.get('type', '') and f.get('url')]
                        if best_stream:
                            url = best_stream[-1]['url']
                            print("🔗 Invidious Network generated direct MP4 link!")
                            stream_download(url, OUTPUT_FILENAME)
                            if verify_success("Invidious Network"): return True
            except: pass
    except Exception as e: print(f"❌ Invidious Failed: {e}")
    return False

# =====================================================================
# APPROACH 2: downr.org Playwright (Native Stealth)
# =====================================================================
async def approach_2_playwright_downr():
    print("\n" + "="*60)
    print("🤖 APPROACH 2: downr.org Scraper (Native Playwright Stealth)")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
            context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = await context.new_page()
            
            # Native stealth override injected directly into the browser
            await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("🌐 Navigating to downr.org...")
            await page.goto("https://downr.org/", timeout=30000)
            
            print("⌨️ Injecting video URL...")
            await page.locator('input[placeholder="Paste URL here"]').fill(TEST_VIDEO_URL)
            await page.locator('button', has_text="Download").first.click()
            
            print("⏳ Waiting for backend processing to generate links (Max 45s)...")
            await page.wait_for_selector('text="mp4 ("', timeout=45000)
            
            for quality in ["1080p", "720p", "480p", "360p"]:
                print(f"🔍 Looking for 'mp4 ({quality})' button...")
                element = page.locator(f'a:has-text("mp4 ({quality})")').first
                if await element.count() > 0:
                    download_url = await element.get_attribute("href")
                    if download_url and "http" in download_url:
                        print(f"🔗 BINGO! Extracted raw MP4 link ({quality})!")
                        stream_download(download_url, OUTPUT_FILENAME, {"Referer": "https://downr.org/"})
                        if verify_success("downr.org Scraper"): return True
    except Exception as e: print(f"❌ Playwright Failed: {str(e).splitlines()[0]}")
    return False

# =====================================================================
# APPROACH 3: Cobalt API via Auto-Scraped Proxies
# =====================================================================
def approach_3_proxy_cobalt():
    print("\n" + "="*60)
    print("🕵️ APPROACH 3: Cobalt API via Public Free Proxies")
    try:
        print("🔍 Fetching fresh proxy list...")
        r = requests.get("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt", timeout=10)
        proxies = r.text.strip().split('\n')
        import random
        random.shuffle(proxies)
        
        headers = {
            "Accept": "application/json", "Content-Type": "application/json",
            "Origin": "https://cobalt.tools", "User-Agent": "Mozilla/5.0"
        }
        payload = {"url": TEST_VIDEO_URL, "vQuality": "1080"}
        
        for proxy in proxies[:10]:
            proxy_url = f"http://{proxy.strip()}"
            print(f"   -> Tunneling API request through: {proxy_url}")
            try:
                res = requests.post("https://api.cobalt.tools/api/json", json=payload, headers=headers, proxies={"http": proxy_url, "https": proxy_url}, timeout=10)
                if res.status_code in [200, 201] and 'url' in res.json():
                    print("🔗 Proxy successfully pierced the firewall!")
                    stream_download(res.json()['url'], OUTPUT_FILENAME)
                    if verify_success("Cobalt API + Proxy Tunnel"): return True
            except: pass
    except Exception as e: print(f"❌ Proxy approach failed: {e}")
    return False

def main():
    print(f"🚀 FIRING FALLBACK TEST FOR: {TEST_VIDEO_URL}\n")
    
    approaches = [
        approach_1_invidious,
        lambda: asyncio.run(approach_2_playwright_downr()),
        approach_3_proxy_cobalt
    ]
    
    for approach in approaches:
        clean_file()
        if approach():
            sys.exit(0)
            
    print("\n💀 ALL APPROACHES DEFEATED. The server is heavily quarantined.")

if __name__ == "__main__":
    main()
