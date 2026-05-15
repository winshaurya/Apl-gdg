import pandas as pd


def add_phase(df):

    def phase(over):
        if over <= 6:
            return "Powerplay"
        elif over <= 15:
            return "Middle"
        else:
            return "Death"

    df["phase"] = df["over"].apply(phase)

    return df


def match_level_features(df):

    match_df = df.groupby(["match_id", "venue", "innings"]).agg({
        "runs": "sum",
        "wicket": "sum"
    }).reset_index()

    return match_df


def player_level_features(df):

    player_df = df.groupby("batter").agg({
        "runs": "sum",
        "ball": "count"
    }).reset_index()

    player_df["strike_rate"] = (player_df["runs"] / player_df["ball"]) * 100

    return player_df


def venue_features(df):

    venue_df = df.groupby("venue").agg({
        "runs": "mean",
        "wicket": "mean"
    }).reset_index()

    return venue_df