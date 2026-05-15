def calculate_impact(df):
    df = df.copy()
    
    df['impact'] = df['runs'] - df['expected_runs']
    
    return df