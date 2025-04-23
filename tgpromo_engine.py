
import os
import subprocess
import sys

# Auto-install required packages if not already installed
try:
    import pyrogram
    import tgcrypto
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyrogram", "tgcrypto"])



import asyncio
import json
import os
from pyrogram import Client
import time

SESSION_NAME = "stranger_auto_spammer"
CRED_FILE = "credentials.json"

def print_banner():
    banner = """[92m
╭━━━━╮╱╱╭━━━╮╱╱╱╱╱╱╱╱╱╱╭╮
┃╭╮╭╮┃╱╱┃╭━╮┃╱╱╱╱╱╱╱╱╱╭╯╰╮
╰╯┃┃┣┻━╮┃╰━╯┣━┳━━┳╮╭┳━┻╮╭╋━━┳━╮
╱╱┃┃┃╭╮┃┃╭━━┫╭┫╭╮┃╰╯┃╭╮┃┃┃┃━┫╭╯
╱╱┃┃┃╰╯┃┃┃╱╱┃┃┃╰╯┃┃┃┃╰╯┃╰┫┃━┫┃
╱╱╰╯╰━╮┃╰╯╱╱╰╯╰━━┻┻┻┻━━┻━┻━━┻╯
╱╱╱╱╭━╯┃
╱╱╱╱╰━━╯
[0m
[93mThis script uses a vulnerability in @RandomMeetBot to promote your message.[0m
[96mCreated by @CyckerX[0m\n
"""
    print(banner)

def load_credentials():
    if os.path.exists(CRED_FILE):
        with open(CRED_FILE, "r") as f:
            creds = json.load(f)
            return creds["api_id"], creds["api_hash"]
    else:
        api_id = int(input("Enter your API ID: ").strip())
        api_hash = input("Enter your API HASH: ").strip()
        with open(CRED_FILE, "w") as f:
            json.dump({"api_id": api_id, "api_hash": api_hash}, f)
        return api_id, api_hash

def get_promo_msg():
    promo = input("Enter your promo message: ").strip()
    if not promo:
        print("Empty promo message not allowed. Exiting.")
        exit()
    return promo

def choose_speed():
    print("\nChoose promotion speed:")
    print("[1] Fast")
    print("[2] Medium")
    print("[3] Slow")
    choice = input("Enter option (1/2/3): ").strip()
    if choice == "1":
        return 1
    elif choice == "2":
        return 3
    elif choice == "3":
        return 5
    else:
        print("Invalid input. Using default Medium speed.")
        return 3

async def wait_for_partner(app):
    print("Waiting for partner...")
    for _ in range(20):
        async for msg in app.get_chat_history("RandomMeetBot", limit=5):
            if msg.text and "🎉You found a partner! 🎊" in msg.text:
                print("Partner found!")
                return True
        await asyncio.sleep(1.5)
    print("No partner found.")
    return False

async def main():
    print_banner()
    api_id, api_hash = load_credentials()
    promo_msg = get_promo_msg()
    delay = choose_speed()

    async with Client(SESSION_NAME, api_id=api_id, api_hash=api_hash) as app:
        count = 0
        while True:
            try:
                await app.send_message("RandomMeetBot", "/chat")
                got_partner = await wait_for_partner(app)

                if got_partner:
                    await asyncio.sleep(1)
                    await app.send_message("RandomMeetBot", promo_msg)
                    print("Promo message sent.")
                    await asyncio.sleep(delay)
                    await app.send_message("RandomMeetBot", "/end")
                    print("Chat ended.")
                    count += 1
                    print(f"Total promos: {count}")
                else:
                    print("Skipping promo...")

                await asyncio.sleep(delay)

            except Exception as e:
                print("Error:", e)
                await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
