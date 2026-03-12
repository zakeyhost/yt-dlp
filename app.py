import os
import time
import yt_dlp

# Configurations
YOUTUBE_COOKIES_PATH = "cookies_yt.txt"
TEST_VIDEO_URL = "https://www.youtube.com/watch?v=QhwR5f-7c5Q"
OUTPUT_FILENAME = "test_video.mp4"

def cleanup_partial_files():
    """Deletes any broken/partial files from a failed attempt before trying the next one."""
    for f in os.listdir('.'):
        if f.startswith('test_video'):
            try:
                os.remove(f)
            except:
                pass

def main():
    print(f"🚀 Starting BRUTE-FORCE yt-dlp test for video: {TEST_VIDEO_URL}")
    print("🛡️ Loading 12 Backup Approaches...\n")
    
    # 10+ UNIQUE BYPASS APPROACHES
    # We test different clients (Android, iOS, TV, VR, Web) and toggle Cookies on/off.
    approaches = [
        {"name": "1. Android App + Cookies", "client": "android", "use_cookies": True},
        {"name": "2. iOS App + Cookies", "client": "ios", "use_cookies": True},
        {"name": "3. Smart TV App + Cookies", "client": "tv", "use_cookies": True},
        {"name": "4. Mobile Web + Cookies", "client": "mweb", "use_cookies": True},
        {"name": "5. Safari Web + Cookies", "client": "web_safari", "use_cookies": True},
        {"name": "6. Android VR + Cookies", "client": "android_vr", "use_cookies": True},
        {"name": "7. Android Creator App + Cookies", "client": "android_creator", "use_cookies": True},
        {"name": "8. TV Embedded + Cookies", "client": "tv_embedded", "use_cookies": True},
        {"name": "9. Internal Combo Fallback + Cookies", "client": "android,ios,tv,mweb", "use_cookies": True},
        {"name": "10. Android App (INCOGNITO / NO COOKIES)", "client": "android", "use_cookies": False},
        {"name": "11. iOS App (INCOGNITO / NO COOKIES)", "client": "ios", "use_cookies": False},
        {"name": "12. Smart TV App (INCOGNITO / NO COOKIES)", "client": "tv", "use_cookies": False},
    ]

    success = False

    for i, approach in enumerate(approaches):
        print("=" * 60)
        print(f"🔄 ATTEMPT {i+1}/12: Using Strategy -> [ {approach['name']} ]")
        print("=" * 60)
        
        cleanup_partial_files() # Wipe broken files from previous failures

        # Base yt-dlp configurations
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': OUTPUT_FILENAME,
            'merge_output_format': 'mp4',
            'quiet': False,
            'no_warnings': True,
            'cachedir': False, # Prevent yt-dlp from remembering previous bot-blocks
            
            # Inject the specific client disguise for this approach
            'extractor_args': {'youtube': [f'player_client={approach["client"]}']},
            'sleep_interval': 2, # Wait 2 seconds to mimic human connection
        }

        # Inject cookies only if this approach calls for it
        if approach["use_cookies"] and os.path.exists(YOUTUBE_COOKIES_PATH):
            print("🍪 Injecting cookies_yt.txt...")
            ydl_opts['cookiefile'] = YOUTUBE_COOKIES_PATH
        elif approach["use_cookies"]:
            print("⚠️ Approach requested cookies, but cookies_yt.txt is missing. Proceeding anyway...")
        else:
            print("🕵️ Stripping cookies (Incognito mode)...")

        try:
            print(f"⬇️ Firing yt-dlp downloader...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([TEST_VIDEO_URL])
            
            # Verify it actually downloaded a file
            if os.path.exists(OUTPUT_FILENAME) and os.path.getsize(OUTPUT_FILENAME) > 0:
                print(f"\n✅ SUCCESS! Approach [{approach['name']}] completely bypassed the block!")
                success = True
                break # EXITS THE LOOP! We got the video!
            else:
                print(f"❌ yt-dlp finished, but the file is missing or empty. Moving to next backup...")
                
        except Exception as e:
            print(f"\n❌ Approach [{approach['name']}] Blocked or Failed.")
            print(f"Error: {e}")
            print("⏳ Switching to next backup method in 3 seconds...\n")
            time.sleep(3) # Short pause so YouTube doesn't completely IP ban the runner

    print("\n" + "=" * 60)
    if success:
        file_size_mb = os.path.getsize(OUTPUT_FILENAME) / (1024 * 1024)
        print(f"🎉 DOWNLOAD SECURED: {file_size_mb:.2f} MB")
        print("GitHub Actions will now upload this file as an artifact so you can download it.")
    else:
        print("💀 ALL 12 APPROACHES FAILED.")
        print("YouTube is heavily blocking this datacenter IP. We may need to use a proxy network.")

if __name__ == "__main__":
    main()
