import os
import sys
import requests
import asyncio
from playwright.async_api import async_playwright

TEST_VIDEO_URL = "https://www.youtube.com/watch?v=QhwR5f-7c5Q"
OUTPUT_FILENAME = "test_video.mp4"

def download_direct(url, filename):
    print("⬇️ Streaming MP4 directly to GitHub Runner...")
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

def approach_1_cobalt_api_fixed():
    print("\n" + "="*50)
    print("👻 APPROACH 1: Cobalt Official API (Fixed Security Headers)")
    print("="*50)
    
    # Cobalt now requires strict headers to prove it's a legitimate request
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://cobalt.tools",
        "Referer": "https://cobalt.tools/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    payload = {
        "url": TEST_VIDEO_URL,
        "vQuality": "1080",
        "filenamePattern": "classic"
    }
    
    instances = [
        "https://api.cobalt.tools", 
        "https://cobalt.envy.wtf",
        "https://api.cobalt.lol"
    ]
    
    for instance in instances:
        print(f"🔌 Connecting to Cobalt instance: {instance}...")
        try:
            res = requests.post(instance, json=payload, headers=headers, timeout=15)
            if res.status_code in [200, 201, 202]:
                data = res.json()
                if 'url' in data:
                    print("✅ Cobalt successfully bypassed YouTube! Extracted raw MP4 link.")
                    return download_direct(data['url'], OUTPUT_FILENAME)
            else:
                print(f"⚠️ Instance failed with status: {res.status_code}. Response: {res.text[:100]}")
        except Exception as e:
            print(f"⚠️ Instance unreachable: {e}")
            
    print("❌ All Cobalt API instances blocked or overloaded.")
    return False

async def approach_2_downr_stealth():
    print("\n" + "="*50)
    print("🤖 APPROACH 2: downr.org Scraper (Playwright Stealth Mode)")
    print("="*50)
    
    async with async_playwright() as p:
        # The arguments below hide the fact that this is an automated bot from Cloudflare
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        
        try:
            print("🌐 Navigating to downr.org...")
            await page.goto("https://downr.org/", timeout=45000)
            
            print("⌨️ Injecting video URL into the search box...")
            await page.get_by_placeholder("Paste URL here").fill(TEST_VIDEO_URL)
            
            print("🖱️ Clicking Download button...")
            await page.get_by_role("button", name="Download").click()
            
            print("⏳ Waiting for backend processing to generate links (Max 45s)...")
            # Wait for the specific section containing "mp4" to render
            await page.wait_for_selector('text="mp4 ("', timeout=45000)
            
            # Target the exact buttons from your screenshot, prioritizing 1080p
            for quality in ["1080p", "720p", "480p", "360p"]:
                print(f"🔍 Looking for 'mp4 ({quality})' button...")
                target_text = f"mp4 ({quality})"
                element = await page.query_selector(f'text="{target_text}"')
                
                if element:
                    download_url = await element.get_attribute("href")
                    if download_url and "http" in download_url:
                        print(f"🔗 BINGO! Extracted raw MP4 link ({quality})!")
                        return download_direct(download_url, OUTPUT_FILENAME)
                    
            print("❌ Could not extract the hidden href link from the buttons.")
        except Exception as e:
            print(f"❌ downr.org Scraper failed: {e}")
        finally:
            await browser.close()
    return False

def main():
    print(f"🚀 Starting STEALTH WEB-SCRAPER test for: {TEST_VIDEO_URL}\n")
    
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)
        
    if approach_1_cobalt_api_fixed():
        sys.exit(0)
        
    if asyncio.run(approach_2_downr_stealth()):
        sys.exit(0)
        
    print("\n💀 ALL BROWSER-SCRAPING APPROACHES FAILED.")

if __name__ == "__main__":
    main()
