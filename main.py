import requests
import os
import json

APIFY_TOKEN = os.environ.get("APIFY_TOKEN")

def run_tiktok_scraper():
    url = "https://api.apify.com/v2/actor-tasks/clockworks~tiktok-profile-scraper/run-sync-get-dataset-items?token=" + APIFY_TOKEN

    payload = {
        "profiles": ["logicalrecovery"],
        "resultsPerPage": 5,
        "shouldDownloadVideos": False
    }


    # Use Apify's actor for TikTok profiles
    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )

    if response.status_code != 200:
        print("Apify call failed:", response.text)
        return

    results = response.json()

    print("\n📊 Video Stats:")
    for item in results:
        print(f"- 🎥 ID: {item.get('id')}")
        print(f"  Description: {item.get('desc')}")
        print(f"  Views: {item.get('stats', {}).get('playCount')}")
        print(f"  Likes: {item.get('stats', {}).get('diggCount')}")
        print(f"  Comments: {item.get('stats', {}).get('commentCount')}")
        print(f"  Shares: {item.get('stats', {}).get('shareCount')}")
        print("---")

if __name__ == "__main__":
    run_tiktok_scraper()
