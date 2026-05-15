from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
from src.pipeline import run_once

app = FastAPI(title="Scriptwriter's Revenge API")


class GenerateRequest(BaseModel):
    match_key: str
    sport: str
    event_id: str
    cricket_fixture: Optional[str] = None
    odds_before: Optional[str] = None
    odds_after: Optional[str] = None
    twitter_fixture: Optional[str] = None


@app.post("/generate")
def generate(payload: GenerateRequest):
    # Leverage the run_once components without importing CLI arg parsing
    from src.ingestion.cricketapi_client import CricketAPIClient
    from src.ingestion.odds_client import OddsAPIClient
    from src.ingestion.twitter_client import TwitterClient
    from src.generator.prompt_builder import build_prompt
    from src.generator.llm_client import LLMClient

    cricket = CricketAPIClient()
    odds = OddsAPIClient()
    twitter = TwitterClient()
    llm = LLMClient()

    match_state = cricket.get_match(payload.match_key, fixture_path=payload.cricket_fixture)
    if payload.odds_before and payload.odds_after:
        before = odds.get_event_odds(payload.sport, payload.event_id, fixture_path=payload.odds_before)
        after = odds.get_event_odds(payload.sport, payload.event_id, fixture_path=payload.odds_after)
        odds_delta = odds.compute_delta(before, after)
    else:
        odds_delta = {}

    twitter_signals = twitter.get_trends_for_match([payload.match_key, "#IPL"], fixture_path=payload.twitter_fixture)

    prompt = build_prompt(match_state, odds_delta, twitter_signals)
    script = llm.generate(prompt)

    return {"prompt": prompt, "script": script}
