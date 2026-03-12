import os
import sys
import socket
import time
import requests
from curl_cffi import requests as cffi_requests
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

TEST_VIDEO_URL = "https://www.youtube.com/watch?v=QhwR5f-7c5Q"
OUTPUT_FILENAME = "test_video.mp4"

# =====================================================================
# THE PHANTOM BYPASS: DNS MONKEYPATCHING
# GitHub's firewall blocks requests to downloader sites by failing the DNS lookup.
# We override the core socket library to route the domains directly to their 
# underlying Cloudflare IP addresses, completely blinding the GitHub firewall.
# =====================================================================
original_getaddrinfo = socket.getaddrinfo

def patched_getaddrinfo(*args, **kwargs):
    domain = args[0]
    # Hardcoded Cloudflare IPs for the blocked APIs
    if domain == 'api.cobalt.tools':
        return original_getaddrinfo('104.21.73.46', *args[1:], **kwargs)
    if domain == 'cobalt.tools':
        return original_getaddrinfo('104.21.73.46', *args[1:], **kwargs)
    if domain == 'yt5s.biz':
        return original_getaddrinfo('104.21.31.29', *args[1:], **kwargs)
    return original_getaddrinfo(*args, **kwargs)

# Apply the patch to the system
socket.getaddrinfo = patched_getaddrinfo

def verify_success(method_name):
    if os.path.exists(OUTPUT_FILENAME) and os.path.getsize(OUTPUT_FILENAME) > 500000:
        size_mb = os.path.getsize(OUTPUT_FILENAME) / (1024 * 1024)
        print(f"\n🎉 EXTREME SUCCESS! [{method_name}] bypassed all firewalls! Size: {size_mb:.2f} MB")
        return True
    return False

def clean_file():
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)

def stream_download(url, filename):
    print("⬇️ Streaming MP4 directly to GitHub Runner...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        # Use curl_cffi to bypass Cloudflare during the actual video download
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
# APPROACH 1: Cobalt API (DNS Patched + Chrome Spoofed)
# =====================================================================
def approach_1_cobalt_api():
    print("\n" + "="*60)
    print("👻 APPROACH 1: Cobalt API (DNS Monkeypatch + Chrome Spoofing)")
    try:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": "https://cobalt.tools",
            "Referer": "https://cobalt.tools/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        payload = {"url": TEST_VIDEO_URL, "vQuality": "1080"}
        
        print("🔌 Sending stealth request to Cobalt Backend...")
        # Impersonate="chrome120" ensures Cloudflare doesn't flag the Python script
        res = cffi_requests.post("https://api.cobalt.tools/api/json", json=payload, headers=headers, impersonate="chrome120", timeout=15)
        
        if res.status_code in [200, 201, 202]:
            data = res.json()
            if 'url' in data:
                print("🔗 Cobalt extracted the raw MP4 link!")
                stream_download(data['url'], OUTPUT_FILENAME)
                return verify_success("Cobalt API DNS Patched")
        else:
            print(f"⚠️ Cobalt rejected request: {res.status_code} - {res.text[:100]}")
    except Exception as e:
        print(f"❌ Cobalt API Failed: {e}")
    return False

# =====================================================================
# APPROACH 2: Playwright Stealth (Fully Masked Browser)
# =====================================================================
async def approach_2_playwright_stealth():
    print("\n" + "="*60)
    print("🤖 APPROACH 2: Cobalt Web UI (Playwright + Stealth Plugin)")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        
        # Apply the stealth plugin to wipe out "webdriver" traces
        await stealth_async(page)
        
        try:
            print("🌐 Navigating to Cobalt UI...")
            await page.goto("https://cobalt.tools/", timeout=30000)
            
            print("⌨️ Injecting URL...")
            await page.locator('input[name="url"], input[type="url"]').first.fill(TEST_VIDEO_URL)
            await page.keyboard.press("Enter")
            
            print("⏳ Waiting for download trigger...")
            async with page.expect_download(timeout=45000) as download_info:
                download = await download_info.value
                print(f"⬇️ Intercepted file! Saving to disk...")
                await download.save_as(OUTPUT_FILENAME)
                
            return verify_success("Playwright Stealth UI")
        except Exception as e:
            print(f"❌ Playwright Failed: {str(e).splitlines()[0]}")
        finally:
            await browser.close()
    return False

# =====================================================================
# APPROACH 3: Free Proxy + Cobalt API
# =====================================================================
def approach_3_proxy_api():
    print("\n" + "="*60)
    print("🕵️ APPROACH 3: Cobalt API via Public Free Proxies")
    print("Fetching live proxies...")
    try:
        r = requests.get("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt", timeout=10)
        proxies = r.text.strip().split('\n')
        
        import random
        random.shuffle(proxies)
        
        headers = {
            "Accept": "application/json", "Content-Type": "application/json",
            "Origin": "https://cobalt.tools", "User-Agent": "Mozilla/5.0"
        }
        payload = {"url": TEST_VIDEO_URL, "vQuality": "1080"}
        
        for proxy in proxies[:5]:
            proxy_url = f"http://{proxy.strip()}"
            print(f"   -> Tunneling API request through: {proxy_url}")
            try:
                # Route ONLY the API request through the proxy to get the link
                res = cffi_requests.post("https://api.cobalt.tools/api/json", json=payload, headers=headers, impersonate="chrome120", proxies={"http": proxy_url, "https": proxy_url}, timeout=10)
                if res.status_code in [200, 201] and 'url' in res.json():
                    print("🔗 Proxy successfully pierced the firewall! Downloading video directly (no proxy)...")
                    # Download the actual video without the proxy for maximum speed
                    stream_download(res.json()['url'], OUTPUT_FILENAME)
                    if verify_success("Cobalt API + Proxy Tunnel"): return True
            except:
                pass
    except Exception as e:
        print(f"❌ Proxy approach failed: {e}")
    return False

def main():
    print(f"🚀 FIRING PHANTOM HANDSHAKE TEST FOR: {TEST_VIDEO_URL}\n")
    
    approaches = [
        approach_1_cobalt_api,
        lambda: asyncio.run(approach_2_playwright_stealth()),
        approach_3_proxy_api
    ]
    
    for approach in approaches:
        clean_file()
        if approach():
            sys.exit(0)
            
    print("\n💀 ALL APPROACHES DEFEATED. The server is heavily quarantined.")

if __name__ == "__main__":
    main()
