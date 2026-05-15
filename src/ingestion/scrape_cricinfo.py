import requests
import pandas as pd
import time


def fetch_match_data(match_id: str):
    url = "https://hs-consumer-api.espncricinfo.com/v1/pages/match/comments"

    all_data = []
    page = 1

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.espncricinfo.com/"
    }

    print(f"🚀 Starting scrape for match_id: {match_id}")

    while True:
        params = {
            "matchId": match_id,
            "page": page
        }

        response = requests.get(url, params=params, headers=headers)

        # 🔍 DEBUG PRINTS (VERY IMPORTANT)
        print(f"\n📄 Page: {page}")
        print(f"Status Code: {response.status_code}")

        if response.status_code != 200:
            print("❌ Request failed or blocked")
            break

        try:
            data = response.json()
        except Exception as e:
            print("❌ JSON parsing error:", e)
            break

        print("Keys in response:", data.keys())

        comments = data.get("comments", [])

        print(f"Number of comments fetched: {len(comments)}")

        # Stop condition
        if not comments:
            print("✅ No more comments. Ending pagination.")
            break

        for ball in comments:
            if "overNumber" not in ball:
                continue

            all_data.append({
                "over": ball.get("overNumber"),
                "ball": ball.get("ballNumber"),
                "batter": ball.get("batsmanName"),
                "bowler": ball.get("bowlerName"),
                "runs": ball.get("runs", 0),
                "wicket": 1 if ball.get("isWicket") else 0,
                "text": ball.get("commentTextItems", [{}])[0].get("commentary", "")
            })

        page += 1
        time.sleep(0.5)  # avoid rate limit

        # Safety break (avoid infinite loop)
        if page > 50:
            print("⚠️ Stopping at 50 pages (safety limit)")
            break

    df = pd.DataFrame(all_data)

    print("\n📊 Final DataFrame Shape:", df.shape)

    if df.empty:
        print("❌ No data collected (likely blocked)")
    else:
        print("✅ Scraping successful")

    return df