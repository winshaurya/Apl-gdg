import os
import sys
from pathlib import Path
import pandas as pd

# Ensure repo root is in sys.path so `from src...` works from any working directory
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ingestion.load_cricsheet import load_match_json


INPUT_PATH = "data/raw/historical/"
OUTPUT_PATH = "data/processed/match_level/historical_data.csv"


def build_dataset():

    all_dfs = []

    files = [f for f in os.listdir(INPUT_PATH) if f.endswith(".json")]

    print(f"📦 Found {len(files)} matches")

    for i, file in enumerate(files):

        try:
            df = load_match_json(os.path.join(INPUT_PATH, file))
            all_dfs.append(df)

            if i % 20 == 0:
                print(f"Processed {i} matches")

        except Exception as e:
            print(f"❌ Error in {file}: {e}")

    full_df = pd.concat(all_dfs, ignore_index=True)

    print("\n✅ Final dataset shape:", full_df.shape)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    full_df.to_csv(OUTPUT_PATH, index=False)

    print(f"💾 Saved at: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_dataset()