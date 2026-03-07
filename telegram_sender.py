#!/usr/bin/env python3

import os
import time
import asyncio
from datetime import datetime

from telegram import Bot
from telegram.error import TelegramError

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/app/screenshots")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))

def get_unsent_screenshots():
    if not os.path.exists(OUTPUT_DIR):
        return []
    
    files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith("screenshot_") and f.endswith(".jpg")]
    files.sort()
    return files

def send_screenshot(bot, chat_id, file_path):
    with open(file_path, "rb") as photo:
         asyncio.run(bot.send_photo(chat_id=chat_id, photo=photo))
    print(f"Sent: {os.path.basename(file_path)}")

def main():
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set")
        return
    
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    
    while True:
        try:
            screenshots = get_unsent_screenshots()
            today = datetime.now().strftime("%Y%m%d")
            
            for filename in screenshots:
                file_path = os.path.join(OUTPUT_DIR, filename)
                
                try:
                    send_screenshot(bot, TELEGRAM_CHAT_ID, file_path)
                    os.remove(file_path)
                    print(f"Sent and deleted: {filename}")
                except TelegramError as e:
                    print(f"Failed to send {filename}: {e}")
                except Exception as e:
                    print(f"Error: {e}")
                    
        except Exception as e:
            print(f"Main loop error: {e}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
