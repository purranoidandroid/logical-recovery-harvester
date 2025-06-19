import os
import requests
import time
from datetime import datetime

def main():
    print("=== Logical Recovery Harvester Started ===")
    now = datetime.utcnow()
    print(f"Current UTC time: {now}")

    apify_token = os.getenv("APIFY_TOKEN")
    username = "logicalrecovery"  # ← replace with your TikTok handle (no @)

    if not apify_token or not username:
        print("❌ Missing APIFY_TOKEN or username. Exiting.")
        return

    # Step 1: Start the Apify Actor for TikTok Profile
    print(f"Launching Apify TikTok scraper for @{username}...")

    start_url = "https://api.apify.com/v2/actor-tasks/ankushdaveri~tiktok-user-scraper/run-sync-get-dataset-items?token={}".format(apify_token)
    payload = {
        "usernames": [username],
        "resultsPerPage": 5,
        "scrollLimit": 1,
        "searchType": "user",
        "downloadVideos": False,
        "shouldDownloadVideo": False,
        "shouldDownloadCover": False
    }

    try:
        response = requests.post(start_url, json=payload)
        data = response.json()

        print(f"✅ Retrieved {len(data)} posts from @{username}\n")
        for i, video in enumerate(data):
    if isinstance(video, dict):
        print(f"--- Video {i+1} ---")
        print(f"ID: {video.get('id')}")
        print(f"Views: {video.get('playCount')}")
        print(f"Likes: {video.get('diggCount')}")
        print(f"Comments: {video.get('commentCount')}")
        print(f"Shares: {video.get('shareCount')}")
        print()
    else:
        print(f"⚠️ Unexpected item at index {i}: {video}")


    except Exception as e:
        print(f"❌ Error fetching from Apify: {e}")

    print("=== Harvester Run Complete ===")

if __name__ == "__main__":
    main()
