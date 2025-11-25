import os
import requests
from datetime import datetime

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
PERSON_URN = os.environ.get("PERSON_URN")
POSTS_FILE = os.environ.get("POSTS_FILE", "posts.txt")

def read_today_post():
    # Day of year (1–365)
    day = datetime.utcnow().timetuple().tm_yday

    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        posts = [line.strip() for line in f.readlines() if line.strip()]

    index = (day - 1) % len(posts)
    return posts[index]

def post_to_linkedin(text):
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    payload = {
        "author": PERSON_URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    print("Response:", response.status_code, response.text)
    response.raise_for_status()

def main():
    post = read_today_post()
    print("Posting:", post)
    post_to_linkedin(post)

if __name__ == "__main__":
    main()

