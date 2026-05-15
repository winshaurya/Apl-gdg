import pandas as pd

def prepare_historical(df_hist):
    df_hist['date'] = pd.to_datetime(df_hist['date'])
    df_hist['year'] = df_hist['date'].dt.year
    return df_hist


def get_match_summary(df_match):
    return {
        "runs": df_match['runs'].sum(),
        "wickets": df_match['wicket'].sum(),
        "venue": df_match['venue'].iloc[0],
        "team1": df_match['team'].unique()[0],
        "team2": df_match['team'].unique()[1] if len(df_match['team'].unique()) > 1 else None
    }


def get_historical_context(df_hist, venue, year_range):
    df_filtered = df_hist[
        (df_hist['venue'] == venue) &
        (df_hist['year'].isin(year_range))
    ]

    if df_filtered.empty:
        return None

    matches = df_filtered['match_id'].nunique()

    return {
        "avg_runs": df_filtered['runs'].sum() / matches,
        "avg_wickets": df_filtered['wicket'].sum() / matches,
        "matches": matches
    }


def compare_with_history(df_match, df_hist):
    df_hist = prepare_historical(df_hist)

    match_summary = get_match_summary(df_match)

    venue = match_summary["venue"]
    match_year = pd.to_datetime(df_match['date'].iloc[0]).year

    # Last year
    last_year = match_year - 1
    last_year_stats = get_historical_context(df_hist, venue, [last_year])

    # Last 5 years
    last_5_years = list(range(match_year - 5, match_year))
    last5_stats = get_historical_context(df_hist, venue, last_5_years)

    return {
        "match": match_summary,
        "last_year": last_year_stats,
        "last_5_years": last5_stats
    }