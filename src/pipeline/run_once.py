"""Stateless runner script for one-shot generation.

Usage:
  python -m src.pipeline.run_once --match-key MATCH_KEY --sport cricket_test --event-id EVENT_ID --dry-run

The runner accepts fixture paths if API keys are not available.
"""
import argparse
import os
import json
from src.ingestion.cricketapi_client import CricketAPIClient
from src.ingestion.odds_client import OddsAPIClient
from src.ingestion.twitter_client import TwitterClient
from src.generator.prompt_builder import build_prompt
from src.generator.llm_client import LLMClient


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--match-key", required=True)
    p.add_argument("--sport", default="cricket_test")
    p.add_argument("--event-id", required=True)
    p.add_argument("--cricket-fixture", help="Path to local match fixture JSON")
    p.add_argument("--odds-before", help="Path to local odds snapshot (before)")
    p.add_argument("--odds-after", help="Path to local odds snapshot (after)")
    p.add_argument("--twitter-fixture", help="Path to local twitter fixture JSON")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    cricket = CricketAPIClient()
    odds = OddsAPIClient()
    twitter = TwitterClient()
    llm = LLMClient()

    match_state = cricket.get_match(args.match_key, fixture_path=args.cricket_fixture)

    if args.odds_before and args.odds_after:
        before = odds.get_event_odds(args.sport, args.event_id, fixture_path=args.odds_before)
        after = odds.get_event_odds(args.sport, args.event_id, fixture_path=args.odds_after)
        odds_delta = odds.compute_delta(before, after)
    else:
        odds_delta = {}

    twitter_signals = twitter.get_trends_for_match([args.match_key, "#IPL"], fixture_path=args.twitter_fixture)

    prompt = build_prompt(match_state, odds_delta, twitter_signals)

    out = llm.generate(prompt)

    result = {
        "match_key": args.match_key,
        "event_id": args.event_id,
        "prompt": prompt,
        "script": out,
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
