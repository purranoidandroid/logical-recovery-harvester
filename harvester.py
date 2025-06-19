import os
from datetime import datetime
from TikTokApi import TikTokApi

def main():
    print("=== Logical Recovery Harvester Started ===")
    now = datetime.utcnow()
    print(f"Current UTC time: {now}")

    session_id = os.getenv("TIKTOK_SESSION_ID")
    username = "logicalrecovery"  # <-- Replace this

    if not session_id:
        print("❌ TikTok session ID not found. Exiting.")
        return

    try:
        with TikTokApi(custom_verify_fp="verify_123", use_test_endpoints=True) as api:
            api._get_cookies()
            api._get_cookies().set("sessionid", session_id, domain=".tiktok.com")

            print(f"Fetching user: {logicalrecovery}")
            user = api.get_user(logicalrecovery=logicalrecovery)

            print("Fetching videos...")
            videos = api.user_posts(user_id=user["user_id"], count=5)

            print(f"Found {len(videos)} videos.\n")
            for i, video in enumerate(videos):
                print(f"--- Video {i+1} ---")
                print(f"ID: {video['id']}")
                print(f"Views: {video['stats']['playCount']}")
                print(f"Likes: {video['stats']['diggCount']}")
                print(f"Comments: {video['stats']['commentCount']}")
                print(f"Shares: {video['stats']['shareCount']}")
                print()

    except Exception as e:
        print(f"❌ Error fetching videos: {e}")

    print("=== Harvester Run Complete ===")

if __name__ == "__main__":
    main()
