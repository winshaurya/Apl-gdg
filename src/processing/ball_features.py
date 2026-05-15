def generate_ball_features(df):
    df = df.copy()
    
    # Phase
    df['phase'] = df['over'].apply(lambda x: "PP" if x <= 6 else "Middle")
    
    # Simple pressure proxy
    df['pressure'] = df['wicket'].cumsum()
    
    return df