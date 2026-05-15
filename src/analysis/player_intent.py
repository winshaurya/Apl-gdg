def calculate_intent(df):

    player_stats = df.groupby("batter").agg({
        "runs": "sum",
        "ball": "count"
    }).reset_index()

    player_stats["strike_rate"] = (player_stats["runs"] / player_stats["ball"]) * 100

    # classify intent
    def classify(sr):
        if sr > 170:
            return "Aggressive"
        elif sr > 130:
            return "Balanced"
        else:
            return "Anchor"

    player_stats["intent"] = player_stats["strike_rate"].apply(classify)

    return player_stats.sort_values("runs", ascending=False)