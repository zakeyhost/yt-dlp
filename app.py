import os
import sys
import requests
import asyncio
from playwright.async_api import async_playwright
from pytubefix import YouTube

TEST_VIDEO_URL = "https://www.youtube.com/watch?v=QhwR5f-7c5Q"
OUTPUT_FILENAME = "test_video.mp4"

def download_direct(url, filename):
    print("⬇️ Streaming MP4 directly to GitHub Runner...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        with requests.get(url, stream=True, headers=headers, timeout=30) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            file_size_mb = os.path.getsize(filename) / (1024 * 1024)
            print(f"✅ SUCCESS! Video secured. Size: {file_size_mb:.2f} MB")
            return True
    except Exception as e:
        print(f"❌ Direct stream failed: {e}")
    return False

async def approach_1_cobalt_web():
    print("\n" + "="*50)
    print("🤖 APPROACH 1: Cobalt WEB UI (Playwright Headless Chrome)")
    print("="*50)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            print("🌐 Navigating to Cobalt.tools web interface...")
            await page.goto("https://cobalt.tools/", timeout=30000)
            
            print("⌨️ Typing video URL into the box...")
            await page.fill('input[id="url-input"]', TEST_VIDEO_URL)
            await page.keyboard.press("Enter")
            print("⏳ Waiting for processing (bypassing CAPTCHAs natively)...")

            # Wait for the download to automatically trigger and intercept it
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

async def approach_2_ssyoutube_web():
    print("\n" + "="*50)
    print("🤖 APPROACH 2: SSYouTube Scraper (Playwright Headless Chrome)")
    print("="*50)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            print("🌐 Navigating to ssyoutube.com...")
            await page.goto("https://ssyoutube.com/en731v/", timeout=30000)
            
            print("⌨️ Injecting video URL...")
            await page.fill('#id_url', TEST_VIDEO_URL)
            await page.click('#search')
            
            print("⏳ Waiting for their servers to generate the MP4 link...")
            await page.wait_for_selector('a.download-icon', timeout=45000)
            download_url = await page.get_attribute('a.download-icon', 'href')
            
            if download_url:
                print("🔗 Extracted raw MP4 link! Downloading...")
                return download_direct(download_url, OUTPUT_FILENAME)
        except Exception as e:
            print(f"❌ SSYouTube Scraper failed: {e}")
        finally:
            await browser.close()
    return False

def approach_3_pytubefix():
    print("\n" + "="*50)
    print("🐍 APPROACH 3: PyTubeFix (Alternative Open-Source Library)")
    print("="*50)
    
    # pytubefix is an actively maintained fork of pytube that bypasses the PO Token differently than yt-dlp
    try:
        print("🔍 Querying YouTube via PyTubeFix...")
        yt = YouTube(TEST_VIDEO_URL, use_po_token=True)
        stream = yt.streams.get_highest_resolution()
        
        print(f"⬇️ Found stream: {stream.resolution}. Downloading...")
        stream.download(filename=OUTPUT_FILENAME)
        
        if os.path.exists(OUTPUT_FILENAME):
            file_size_mb = os.path.getsize(OUTPUT_FILENAME) / (1024 * 1024)
            print(f"✅ SUCCESS! PyTubeFix bypassed the block. Size: {file_size_mb:.2f} MB")
            return True
    except Exception as e:
        print(f"❌ PyTubeFix failed: {e}")
    return False

def main():
    print(f"🚀 Starting WEB-SCRAPER DOWNLOAD test for: {TEST_VIDEO_URL}\n")
    
    # Clean up any partial files
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)
        
    if asyncio.run(approach_1_cobalt_web()):
        sys.exit(0)
        
    if asyncio.run(approach_2_ssyoutube_web()):
        sys.exit(0)
        
    if approach_3_pytubefix():
        sys.exit(0)
        
    print("\n💀 ALL BROWSER-SCRAPING APPROACHES FAILED.")

if __name__ == "__main__":
    main()
