import numpy as np
import pandas as pd


def assign_zones(df):
    
    # Approximate length using ball progression (proxy)
    df["zone"] = pd.cut(
        df["ball"],
        bins=[0, 2, 4, 6],
        labels=["Full", "Good Length", "Short"]
    )

    return df


def zone_performance(df):

    zone_stats = df.groupby("zone").agg({
        "runs": "sum",
        "wicket": "sum",
        "ball": "count"
    }).reset_index()

    zone_stats["economy"] = zone_stats["runs"] / zone_stats["ball"] * 6

    return zone_stats