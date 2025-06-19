import requests
import os
import json
import time

APIFY_TOKEN = os.environ.get("APIFY_TOKEN")
USERNAME = "logicalrecovery"

def run_tiktok_scraper():
    print("=== Logical Recovery Harvester Started ===")

    # Step 1: Launch actor run directly (not via task)
    start_url = f"https://api.apify.com/v2/acts/clockworks~tiktok-profile-scraper/runs?token={APIFY_TOKEN}"

    payload = {
        "profiles": [USERNAME],
        "resultsPerPage": 5,
        "shouldDownloadVideos": False
    }

    headers = {
        "Content-Type": "application/json"
    }

    start_response = requests.post(start_url, headers=headers, data=json.dumps(payload))

    if start_response.status_code != 201:
        print("❌ Failed to launch Apify actor:", start_response.text)
        return

    run_id = start_response.json().get("id")
    print(f"🎬 Actor launched with run ID: {run_id}")

    # Step 2: Wait a few seconds for it to finish
    time.sleep(10)

    # Step 3: Get dataset results
    dataset_url = f"https://api.apify.com/v2/actor-runs/{run_id}/dataset/items?token={APIFY_TOKEN}&clean=true"
    data_response = requests.get(dataset_url)

    if data_response.status_code != 200:
        print("❌ Failed to fetch dataset results:", data_response.text)
        return

    results = data_response.json()

    print("\n📊 Video Stats:")
    for i, item in enumerate(results):
        print(f"--- Video {i+1} ---")
        print(f"ID: {item.get('id')}")
        print(f"Description: {item.get('desc')}")
        print(f"Views: {item.get('stats', {}).get('playCount')}")
        print(f"Likes: {item.get('stats', {}).get('diggCount')}")
        print(f"Comments: {item.get('stats', {}).get('commentCount')}")
        print(f"Shares: {item.get('stats', {}).get('shareCount')}")
        print("---")

if __name__ == "__main__":
    run_tiktok_scraper()
