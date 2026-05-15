import pandas as pd


def build_match_summary(df):
    return {
        "total_runs": int(df["runs"].sum()),
        "total_wickets": int(df["wicket"].sum()),
        "venue": df["venue"].iloc[0],
        "top_batter": df.groupby("batter")["runs"].sum().idxmax(),
        "top_bowler": df.groupby("bowler")["wicket"].sum().idxmax()
    }


def build_historical_context(df_match, df_hist):
    venue = df_match["venue"].iloc[0]

    df_hist['date'] = pd.to_datetime(df_hist['date'])
    df_hist['year'] = df_hist['date'].dt.year

    current_year = pd.to_datetime(df_match['date'].iloc[0]).year

    last5 = df_hist[
        (df_hist["venue"] == venue) &
        (df_hist["year"] < current_year) &
        (df_hist["year"] >= current_year - 5)
    ]

    if last5.empty:
        return {}

    matches = last5["match_id"].nunique()

    return {
        "avg_runs": round(last5["runs"].sum() / matches, 2),
        "avg_wickets": round(last5["wicket"].sum() / matches, 2)
    }


def build_player_context(df_match, df_hist):

    top_batter = df_match.groupby("batter")["runs"].sum().idxmax()

    player_hist = df_hist[df_hist["batter"] == top_batter]

    if player_hist.empty:
        return {}

    matches = player_hist["match_id"].nunique()

    return {
        "player": top_batter,
        "avg_runs": round(player_hist["runs"].sum() / matches, 2)
    }


def build_context_string(summary, hist_ctx, player_ctx):

    return f"""
CURRENT MATCH:
- Total Runs: {summary['total_runs']}
- Total Wickets: {summary['total_wickets']}
- Venue: {summary['venue']}
- Top Batter: {summary['top_batter']}
- Top Bowler: {summary['top_bowler']}

HISTORICAL CONTEXT:
- Avg Runs (last 5 yrs at venue): {hist_ctx.get('avg_runs', 'NA')}
- Avg Wickets: {hist_ctx.get('avg_wickets', 'NA')}

PLAYER CONTEXT:
- Player: {player_ctx.get('player', 'NA')}
- Avg Runs (historical): {player_ctx.get('avg_runs', 'NA')}

TASK:
Give 3-5 deep insights:
- Highlight anomalies
- Compare with historical benchmarks
- Identify unexpected patterns
- Avoid generic commentary
"""