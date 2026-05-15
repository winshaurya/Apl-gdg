def calculate_surge(df):
    
    # runs per over
    over_runs = df.groupby("over")["runs"].sum().reset_index()

    # rolling avg baseline
    over_runs["expected"] = over_runs["runs"].rolling(3, min_periods=1).mean()

    # surge
    over_runs["surge"] = over_runs["runs"] - over_runs["expected"]

    return over_runs