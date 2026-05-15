import sys
import os

# Add parent directory to path so src module can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestion.load_cricsheet import load_match_json

# Use local JSON file instead of scraping (ESPN API is blocked)
df = load_match_json("data/raw/historical/1082591.json")

print(df.head())
print(df.shape)