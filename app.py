import os
import sys
import requests
import asyncio
from playwright.async_api import async_playwright

TEST_VIDEO_URL = "https://www.youtube.com/watch?v=QhwR5f-7c5Q"
OUTPUT_FILENAME = "test_video.mp4"

def download_direct(url, filename):
    print("⬇️ Streaming MP4 directly to GitHub Runner...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://downr.org/"
    }
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

async def approach_1_downr_stealth():
    print("\n" + "="*50)
    print("🤖 APPROACH 1: downr.org Scraper (Playwright Stealth Mode)")
    print("="*50)
    
    async with async_playwright() as p:
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
            # STRICT MODE FIX: We target the main button and force it to only pick the first one it sees.
            await page.locator('button', has_text="Download").first.click()
            
            print("⏳ Waiting for backend processing to generate links (Max 45s)...")
            await page.wait_for_selector('text="mp4 ("', timeout=45000)
            
            # Target the exact buttons from your screenshot, prioritizing 1080p
            for quality in ["1080p", "720p", "480p", "360p"]:
                print(f"🔍 Looking for 'mp4 ({quality})' button...")
                
                # Look for an 'a' (link) tag that contains the exact text
                element = page.locator(f'a:has-text("mp4 ({quality})")').first
                
                if await element.count() > 0:
                    download_url = await element.get_attribute("href")
                    if download_url and "http" in download_url:
                        print(f"🔗 BINGO! Extracted raw MP4 link ({quality})!")
                        if download_direct(download_url, OUTPUT_FILENAME):
                            return True
                    
            print("❌ Could not extract the hidden href link from the buttons.")
        except Exception as e:
            print(f"❌ downr.org Scraper failed: {e}")
        finally:
            await browser.close()
    return False

async def approach_2_cobalt_web():
    print("\n" + "="*50)
    print("🤖 APPROACH 2: Cobalt WEB UI (Dynamic Locator Fix)")
    print("="*50)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = await context.new_page()
        
        try:
            print("🌐 Navigating to Cobalt.tools web interface...")
            await page.goto("https://cobalt.tools/", timeout=30000)
            
            print("⌨️ Typing video URL into the box...")
            # DYNAMIC FIX: Cobalt changed their input ID. This finds ANY url input box.
            await page.locator('input[type="url"], input[name="url"], input').first.fill(TEST_VIDEO_URL)
            await page.keyboard.press("Enter")
            print("⏳ Waiting for processing (bypassing CAPTCHAs natively)...")

            # Wait for the download to automatically trigger
            async with page.expect_download(timeout=60000) as download_info:
                download = await download_info.value
                print(f"⬇️ Intercepted Download! Saving to {OUTPUT_FILENAME}...")
                await download.save_as(OUTPUT_FILENAME)

            if os.path.exists(OUTPUT_FILENAME):
                file_size_mb = os.path.getsize(OUTPUT_FILENAME) / (1024 * 1024)
                print(f"✅ SUCCESS! Playwright extracted the video. Size: {file_size_mb:.2f} MB")
                return True
        except Exception as e:
            print(f"❌ Cobalt Web Scraper failed: {e}")
        finally:
            await browser.close()
    return False

def main():
    print(f"🚀 Starting STEALTH WEB-SCRAPER test for: {TEST_VIDEO_URL}\n")
    
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)
        
    if asyncio.run(approach_1_downr_stealth()):
        sys.exit(0)
        
    if asyncio.run(approach_2_cobalt_web()):
        sys.exit(0)
        
    print("\n💀 ALL BROWSER-SCRAPING APPROACHES FAILED.")

if __name__ == "__main__":
    main()
