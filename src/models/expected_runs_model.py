def add_expected_runs(df):
    df = df.copy()
    
    # Dummy baseline (upgrade later)
    df['expected_runs'] = 1.2
    
    return df