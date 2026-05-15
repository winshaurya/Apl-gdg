import json
import pandas as pd


def load_match_json(file_path):

    with open(file_path) as f:
        data = json.load(f)

    rows = []

    # Metadata
    venue = data["info"].get("venue", "Unknown")
    teams = data["info"].get("teams", [])
    match_date = data["info"].get("dates", ["Unknown"])[0]
    city = data["info"].get("city", "Unknown")

    for inning_idx, inning in enumerate(data["innings"], start=1):

        # support 2 flavors:
        # 1) legacy CricSheet: {'team': {...}} per inning
        # 2) modern format: {'team': 'X', 'overs': [...]}
        if isinstance(inning, dict) and "overs" in inning and "team" in inning:
            team = inning.get("team", "Unknown")
            overs = inning.get("overs", [])
        else:
            team, details = next(iter(inning.items()))
            overs = details.get("overs", [])

        for over_data in overs:
            over = over_data.get("over")
            ball_counter = 0

            for delivery_item in over_data.get("deliveries", []):
                ball_counter += 1

                if isinstance(delivery_item, dict) and "batter" in delivery_item and "bowler" in delivery_item:
                    delivery = delivery_item
                    # Format to 0.1, 0.2 from over 0, 1.1 from over 1 etc
                    ball_num = float(f"{int(over)}.{ball_counter}") if over is not None else float(ball_counter)
                else:
                    ball_key = list(delivery_item.keys())[0]
                    ball_num = float(ball_key)
                    delivery = delivery_item[ball_key]

                runs = delivery.get("runs", {})
                batter_runs = runs.get("batter", 0)
                extras = runs.get("extras", 0)

                rows.append({
                        "match_id": file_path.split("/")[-1].replace(".json", ""),
                        "venue": venue,
                        "city": city,
                        "date": match_date,
                        "innings": inning_idx,
                        "team": team,
                        "over": over,
                        "ball": ball_num,
                        "batter": delivery.get("batter", ""),
                        "bowler": delivery.get("bowler", ""),
                        "runs": batter_runs + extras,
                        "wicket": len(delivery.get("wickets", []))
                    })

    return pd.DataFrame(rows)