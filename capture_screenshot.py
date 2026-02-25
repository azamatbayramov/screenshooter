#!/usr/bin/env python3

import os
import time
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

STREAM_URL = os.getenv("STREAM_URL", "https://ucams.ufanet.ru/api/internal/embed/1698819642ZKC391/?ttl=3600&mute=true")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/app/screenshots")
INTERVAL = int(os.getenv("INTERVAL", "3600"))

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_last_screenshot_time():
    files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith("screenshot_") and f.endswith(".jpg")]
    if not files:
        return None
    files.sort()
    last_file = os.path.join(OUTPUT_DIR, files[-1])
    return os.path.getmtime(last_file)

def capture_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(STREAM_URL, wait_until="networkidle", timeout=30000)
            time.sleep(3)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(OUTPUT_DIR, f"screenshot_{timestamp}.jpg")
            
            page.screenshot(path=output_file, quality=85)
            print(f"Screenshot saved: {output_file}")
            
        except Exception as e:
            print(f"Failed to capture screenshot: {e}")
        
        browser.close()

def should_capture():
    last_time = get_last_screenshot_time()
    if last_time is None:
        return True
    
    elapsed = time.time() - last_time
    return elapsed >= INTERVAL

if __name__ == "__main__":
    while True:
        if should_capture():
            capture_screenshot()
        else:
            last_time = get_last_screenshot_time()
            next_capture = INTERVAL - (time.time() - last_time)
            print(f"Next screenshot in {int(next_capture)} seconds")
        
        time.sleep(60)