#!/usr/bin/env python3

import os
import time
from datetime import datetime, timedelta

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/app/screenshots")
MAX_AGE_HOURS = int(os.getenv("MAX_AGE_HOURS", "168"))

def cleanup_old_screenshots():
    if not os.path.exists(OUTPUT_DIR):
        print(f"Directory {OUTPUT_DIR} does not exist")
        return
    
    files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith("screenshot_") and f.endswith(".jpg")]
    if not files:
        print("No screenshots to clean up")
        return
    
    cutoff_time = time.time() - (MAX_AGE_HOURS * 3600)
    deleted_count = 0
    
    for filename in files:
        file_path = os.path.join(OUTPUT_DIR, filename)
        if os.path.getmtime(file_path) < cutoff_time:
            os.remove(file_path)
            deleted_count += 1
            print(f"Deleted: {filename}")
    
    print(f"Cleanup complete. Deleted {deleted_count} files")

if __name__ == "__main__":
    while True:
        cleanup_old_screenshots()
        time.sleep(3600)