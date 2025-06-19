import os
from datetime import datetime
from TikTokApi import TikTokApi

def main():
    print("=== Logical Recovery Harvester Started ===")
    now = datetime.utcnow()
    print(f"Current UTC time: {now}")

    session_id = os.getenv("TIKTOK_SESSION_ID")
    if not session_id:
        print("❌ TikTok session ID not found. Exiting.")
        return

    try:
        api = TikTokApi()
        api.cookies.set_cookie("sessionid", session_id, domain=".tiktok.com")

        # Replace this with your TikTok username
        username = "logicalrecovery"

        print(f"Fetching videos for user: {logicalrecovery}")
        user = api.user(logicalrecovery=logicalrecovery)
        videos = user.videos(count=5)

        print(f"Found {len(videos)} videos.")
        for i, video in enumerate(videos):
            print(f"--- Video {i+1} ---")
            print(f"ID: {video.id}")
            print(f"Views: {video.stats.view_count}")
            print(f"Likes: {video.stats.digg_count}")
            print(f"Comments: {video.stats.comment_count}")
            print(f"Shares: {video.stats.share_count}")
            print()

    except Exception as e:
        print(f"❌ Error while fetching TikTok data: {e}")

    print("=== Harvester Run Complete ===")

if __name__ == "__main__":
    main()
