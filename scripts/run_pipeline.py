import sys
import os

# Fix import path
sys.path.append(os.path.abspath("."))

import pandas as pd

# -----------------------------
# IMPORTS
# -----------------------------
from src.ingestion.load_cricsheet import load_match_json
from src.processing.clean_data import clean_data
from src.processing.ball_features import generate_ball_features
from src.models.expected_runs_model import add_expected_runs
from src.models.impact_model import calculate_impact
from src.visualization.run_rate_graph import plot_run_rate
from src.analysis.context_builder import (
    build_match_summary,
    build_historical_context,
    build_player_context,
    build_context_string
)

from src.analysis.insight_generator import generate_insights

from src.analysis.historical_compare import compare_with_history


# -----------------------------
# CONFIG
# -----------------------------
DATA_PATH = "data/raw/historical/"
HISTORICAL_PATH = "data/processed/match_level/historical_data.csv"

OUTPUT_CHART_PATH = "outputs/charts/"
OUTPUT_TEXT_PATH = "outputs/linkedin_assets/"


# -----------------------------
# PIPELINE FUNCTION
# -----------------------------
def run_pipeline(match_id: str):

    print(f"\n🚀 Running pipeline for match: {match_id}")

    # -----------------------------
    # 1. LOAD DATA
    # -----------------------------
    file_path = f"{DATA_PATH}{match_id}.json"

    if not os.path.exists(file_path):
        print(f"❌ Match file not found: {file_path}")
        return

    print("📥 Loading data...")
    df = load_match_json(file_path)
    print("Shape after load:", df.shape)

    # -----------------------------
    # 2. CLEAN DATA
    # -----------------------------
    print("🧹 Cleaning data...")
    df = clean_data(df)

    # -----------------------------
    # 3. FEATURE ENGINEERING
    # -----------------------------
    print("⚙️ Generating features...")
    df = generate_ball_features(df)

    # -----------------------------
    # 4. EXPECTED RUNS
    # -----------------------------
    print("📊 Adding expected runs...")
    df = add_expected_runs(df)

    # -----------------------------
    # 5. IMPACT METRIC
    # -----------------------------
    print("🔥 Calculating impact...")
    df = calculate_impact(df)

    # -----------------------------
    # 6. VISUALIZATION
    # -----------------------------
    print("📈 Generating run rate chart...")

    os.makedirs(OUTPUT_CHART_PATH, exist_ok=True)

    chart_path = f"{OUTPUT_CHART_PATH}{match_id}_runrate.png"
    plot_run_rate(df, save_path=chart_path)

    print(f"📁 Chart saved: {chart_path}")

    # -----------------------------
    # 7. MATCH SUMMARY
    # -----------------------------
    print("🧠 Creating match summary...")

    total_runs = df["runs"].sum()
    total_wickets = df["wicket"].sum()

    top_batter = df.groupby("batter")["runs"].sum().idxmax()
    top_bowler = df.groupby("bowler")["wicket"].sum().idxmax()

    venue = df["venue"].iloc[0] if "venue" in df.columns else "Unknown"

    summary = f"""
Match Summary:
Venue: {venue}
Total Runs: {total_runs}
Total Wickets: {total_wickets}
Top Batter: {top_batter}
Top Bowler: {top_bowler}
"""

    print(summary)

    # -----------------------------
    # 8. HISTORICAL COMPARISON
    # -----------------------------
    print("📊 Comparing with historical data...")

    if not os.path.exists(HISTORICAL_PATH):
        print("⚠️ Historical dataset not found. Skipping comparison.")
        comparative_insights = []
    else:
        df_hist = pd.read_csv(HISTORICAL_PATH)

        comparison = compare_with_history(df, df_hist)

        comparative_insights = "Using context-based insights instead"

    # -----------------------------
    # 9. AI INSIGHTS (OPTIONAL)
    # -----------------------------
    print("🧠 Building structured context...")

    summary_dict = build_match_summary(df)

    df_hist = pd.read_csv(HISTORICAL_PATH)

    hist_ctx = build_historical_context(df, df_hist)
    player_ctx = build_player_context(df, df_hist)

    context = build_context_string(summary_dict, hist_ctx, player_ctx)

    print("\n📦 CONTEXT SENT TO GEMINI:\n")
    print(context)

    print("\n🤖 Generating AI insights...")

    ai_insights = generate_insights(context)

    # -----------------------------
    # 10. PRINT INSIGHTS
    # -----------------------------
    print("\n🔥 COMPARATIVE INSIGHTS:\n")
    if isinstance(comparative_insights, str):
        print(comparative_insights)
    else:
        for i, ins in enumerate(comparative_insights, 1):
            print(f"{i}. {ins}")

    print("\n🤖 AI INSIGHTS:\n")
    print(ai_insights)

    # -----------------------------
    # 11. SAVE OUTPUT
    # -----------------------------
    os.makedirs(OUTPUT_TEXT_PATH, exist_ok=True)

    output_file = f"{OUTPUT_TEXT_PATH}{match_id}_insights.txt"

    with open(output_file, "w") as f:
        f.write("MATCH CONTEXT:\n")
        f.write(context)

        f.write("\n\nAI INSIGHTS:\n")
        f.write(ai_insights)

    print(f"\n📁 Insights saved at: {output_file}")

    print("\n✅ PIPELINE COMPLETE\n")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("1. python run_pipeline.py 1082591")
        print("2. python run_pipeline.py latest")
        print('3. python run_pipeline.py live "RCB vs SRH"')

    elif sys.argv[1] == "latest":
        df = pd.read_csv("data/processed/match_level/historical_data.csv")
        df['date'] = pd.to_datetime(df['date'])

        latest_match = df.sort_values("date", ascending=False)['match_id'].iloc[0]
        run_pipeline(str(latest_match))

    elif sys.argv[1] == "live":
        match_name = sys.argv[2]

        from src.analysis.live_insights import generate_live_match_insights

        generate_live_match_insights(match_name)

    else:
        match_id = sys.argv[1]
        run_pipeline(match_id)