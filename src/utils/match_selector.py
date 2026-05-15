import pandas as pd

HIST_PATH = "data/processed/match_level/historical_data.csv"

TEAM_MAP = {
    "RCB": "Royal Challengers Bengaluru",
    "SRH": "Sunrisers Hyderabad",
    "MI": "Mumbai Indians",
    "CSK": "Chennai Super Kings",
    "KKR": "Kolkata Knight Riders",
    "DC": "Delhi Capitals",
    "PBKS": "Punjab Kings",
    "RR": "Rajasthan Royals"
}


def normalize_team(team):
    if team.upper() in TEAM_MAP:
        return TEAM_MAP[team.upper()]
    return team


def get_match_id_by_input(team1=None, team2=None, date=None):

    df = pd.read_csv(HIST_PATH)
    df['date'] = pd.to_datetime(df['date'])

    # Normalize teams
    if team1:
        team1 = normalize_team(team1)
    if team2:
        team2 = normalize_team(team2)

    # Filter
    if date:
        df = df[df['date'] == pd.to_datetime(date)]

    if team1:
        df = df[df['team'].str.contains(team1, case=False, na=False)]

    if team2:
        df = df[df['team'].str.contains(team2, case=False, na=False)]

    if df.empty:
        print("❌ No match found with given filters")
        print(f"👉 team1={team1}, team2={team2}, date={date}")
        return None

    # Pick first match
    match_id = df['match_id'].iloc[0]

    print(f"✅ Match found: {match_id}")
    print(df[['match_id', 'team', 'date']].drop_duplicates().head())

    return str(match_id)