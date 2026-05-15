def clean_data(df):
    df = df.copy()
    df['total_runs'] = df['runs']
    return df