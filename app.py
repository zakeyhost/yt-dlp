import os
import sys
import time
from curl_cffi import requests as cffi_requests

TEST_VIDEO_URL = "https://www.youtube.com/watch?v=QhwR5f-7c5Q"
TEST_VIDEO_ID = "QhwR5f-7c5Q"
OUTPUT_FILENAME = "test_video.mp4"

def clean_file():
    if os.path.exists(OUTPUT_FILENAME):
        os.remove(OUTPUT_FILENAME)

def verify_success(method_name):
    # Verify the file was created and is larger than 500KB (to ensure it's not an HTML error page)
    if os.path.exists(OUTPUT_FILENAME) and os.path.getsize(OUTPUT_FILENAME) > 500000:
        size_mb = os.path.getsize(OUTPUT_FILENAME) / (1024 * 1024)
        print(f"\n🎉 EXTREME SUCCESS! [{method_name}] bypassed all firewalls! Size: {size_mb:.2f} MB")
        return True
    return False

def stream_download(url, filename):
    print("⬇️ Streaming MP4 directly to GitHub Runner...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        # Impersonate="chrome120" makes the Python TLS fingerprint mathematically identical to Google Chrome
        with cffi_requests.get(url, stream=True, headers=headers, impersonate="chrome120", timeout=60) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk: f.write(chunk)
        return True
    except Exception as e:
        print(f"❌ Direct stream failed: {e}")
    return False

# =====================================================================
# APPROACH 1: The Piped Network (Decentralized YouTube Proxy)
# =====================================================================
def approach_1_piped_network():
    print("\n" + "="*60)
    print("🌍 APPROACH 1: Piped API (Ultimate YouTube Proxy Network)")
    print("="*60)
    
    # Public Piped instances. These servers bypass BotGuard and PO Tokens on their end.
    instances = [
        "https://pipedapi.kavin.rocks",
        "https://pipedapi.tokhmi.xyz",
        "https://pipedapi.syncpundit.io",
        "https://piped-api.garudalinux.org"
    ]
    
    for instance in instances:
        print(f"   -> Pinging Piped Instance: {instance}...")
        try:
            # We use Chrome 120 impersonation to bypass any Cloudflare on the Piped instance
            res = cffi_requests.get(f"{instance}/streams/{TEST_VIDEO_ID}", impersonate="chrome120", timeout=15)
            if res.status_code == 200:
                data = res.json()
                streams = data.get("videoStreams", [])
                
                # Find a stream that contains both Video and Audio (Muxed)
                valid_streams = [s for s in streams if not s.get("videoOnly") and s.get("url")]
                
                if valid_streams:
                    best_stream = valid_streams[-1] # Grabs the highest quality muxed stream
                    print(f"🔗 Piped Network generated a direct proxy link! (Quality: {best_stream.get('quality')})")
                    stream_download(best_stream['url'], OUTPUT_FILENAME)
                    
                    if verify_success(f"Piped Network ({instance})"): return True
            else:
                print(f"      ⚠️ Instance returned status: {res.status_code}")
        except Exception as e:
            print(f"      ⚠️ Connection failed: {str(e).splitlines()[0]}")
            
    return False

# =====================================================================
# APPROACH 2: Loader.to Backend API (TLS Spoofed)
# =====================================================================
def approach_2_loader_to():
    print("\n" + "="*60)
    print("🚀 APPROACH 2: Loader.to Backend (TLS Spoofing via curl_cffi)")
    print("="*60)
    try:
        url = f"https://p.loader.to/ajax/download.php?format=1080&url={TEST_VIDEO_URL}"
        print("🔍 Sending Chrome-Spoofed AJAX request...")
        res = cffi_requests.get(url, impersonate="chrome120", timeout=15).json()
        
        if not res.get("success"):
            print("❌ Loader.to rejected the initial request.")
            return False
            
        task_id = res.get("id")
        print("⏳ Server is processing the video... Polling...")
        
        for _ in range(12): # Poll for up to 60 seconds
            time.sleep(5)
            prog = cffi_requests.get(f"https://p.loader.to/ajax/progress.php?id={task_id}", impersonate="chrome120", timeout=10).json()
            print(f"   -> Status: {prog.get('text')} ({prog.get('progress', 0)/10}%)")
            
            if prog.get("download_url"):
                print("🔗 BINGO! Loader.to link extracted!")
                stream_download(prog["download_url"], OUTPUT_FILENAME)
                if verify_success("Loader.to CFFI"): return True
    except Exception as e: 
        print(f"❌ Failed: {e}")
    return False

# =====================================================================
# APPROACH 3: Cobalt Backend API (TLS Spoofed)
# =====================================================================
def approach_3_cobalt_cffi():
    print("\n" + "="*60)
    print("👻 APPROACH 3: Cobalt Backend (TLS Spoofing via curl_cffi)")
    print("="*60)
    try:
        instances = [
            "https://co.wuk.sh",
            "https://api.cobalt.tools",
            "https://cobalt.envy.wtf"
        ]
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {"url": TEST_VIDEO_URL, "vQuality": "1080"}
        
        for instance in instances:
            print(f"   -> Attacking Cobalt Instance: {instance}...")
            try:
                # Format the URL based on the instance structure
                url = f"{instance}/api/json" if "tools" in instance else instance
                
                # Critical headers to bypass Cobalt's new API locks
                headers["Origin"] = instance
                headers["Referer"] = f"{instance}/"
                
                res = cffi_requests.post(url, json=payload, headers=headers, impersonate="chrome120", timeout=15)
                
                if res.status_code in [200, 201, 202] and 'url' in res.json():
                    print("🔗 Cobalt extracted the link!")
                    stream_download(res.json()['url'], OUTPUT_FILENAME)
                    if verify_success(f"Cobalt CFFI ({instance})"): return True
            except: pass
    except Exception as e: 
        print(f"❌ Failed: {e}")
    return False

def main():
    print(f"🚀 FIRING THE PIPED NETWORK TEST FOR: {TEST_VIDEO_URL}\n")
    
    approaches = [
        approach_1_piped_network,
        approach_2_loader_to,
        approach_3_cobalt_cffi
    ]
    
    for approach in approaches:
        clean_file()
        if approach():
            sys.exit(0)
            
    print("\n💀 ALL APPROACHES DEFEATED. The datacenter ban remains unpierced.")

if __name__ == "__main__":
    main()
