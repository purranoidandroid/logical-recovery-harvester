import requests
import os
import json
import time

APIFY_TOKEN = os.environ.get("APIFY_TOKEN")
USERNAME = "logicalrecovery"

def run_tiktok_scraper():
    print("=== Logical Recovery Harvester Started ===")

    # Step 1: Launch actor directly (not via task)
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

    # Step 2: Poll until the actor run is complete
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={APIFY_TOKEN}"
    max_wait = 60  # seconds
    waited = 0

    while waited < max_wait:
        status_response = requests.get(status_url)
        status_data = status_response.json()
        status = status_data.get("status")

        if status == "SUCCEEDED":
            print("✅ Apify actor run completed.")
            break
        elif status == "FAILED":
            print("❌ Apify actor run failed.")
            return
        else:
            print(f"⏳ Waiting for run to finish... ({status})")
            time.sleep(5)
            waited += 5
    else:
        print("❌ Timed out waiting for Apify run.")
        return

    # Step 3: Get dataset results
    dataset_url = f"https://api.apify.com/v2/actor-runs/{run_id}/dataset/items?token={APIFY_TOKEN}&clean=true"
    data_response = requests.get(dataset_url)

    if data_response.status_code != 200:
        print("❌ Failed to fetch dataset results:", data_response.text)
        return

    results = data_response.json()

    print("\n📊 Video Stats:")
    for i, item in enumerate(results):
        if isinstance(item, dict):
            print(f"--- Video {i+1} ---")
            print(f"ID: {item.get('id')}")
            print(f"Description: {item.get('desc')}")
            print(f"Views: {item.get('stats', {}).get('playCount')}")
            print(f"Likes: {item.get('stats', {}).get('diggCount')}")
            print(f"Comments: {item.get('stats', {}).get('commentCount')}")
            print(f"Shares: {item.get('stats', {}).get('shareCount')}")
            print("---")
        else:
            print(f"⚠️ Unexpected item at index {i}: {item}")

if __name__ == "__main__":
    run_tiktok_scraper()
