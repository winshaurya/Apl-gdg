import os
import json
import time
import requests
from typing import Dict, Any, Optional, List


class OddsAPIClient:
    """Client for The Odds API (stateless)."""

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.the-odds-api.com/v4"):
        self.api_key = api_key or os.getenv("ODDS_API_KEY")
        self.base_url = base_url.rstrip("/")

    def _get(self, path: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        params = params or {}
        if self.api_key:
            params.setdefault("apiKey", self.api_key)
        url = f"{self.base_url}/{path.lstrip('/')}"
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()

    def load_fixture(self, fixture_path: str) -> Any:
        with open(fixture_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_event_odds(self, sport: str, event_id: str, fixture_path: Optional[str] = None) -> Dict[str, Any]:
        if fixture_path and not self.api_key:
            return self.load_fixture(fixture_path)
        return self._get(f"sports/{sport}/events/{event_id}/odds")

    def compute_delta(self, before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
        """Compute simple per-bookmaker delta for h2h prices between two snapshots.

        Returns a compact dict keyed by bookmaker with before/after prices.
        """
        def extract_prices(snapshot: Dict[str, Any]) -> Dict[str, float]:
            out = {}
            for b in snapshot.get("bookmakers", []):
                key = b.get("key")
                # find h2h market
                for m in b.get("markets", []):
                    if m.get("key") == "h2h":
                        # outcomes: list of {name, price}
                        prices = {o["name"]: o.get("price") for o in m.get("outcomes", [])}
                        out[key] = prices
            return out

        p_before = extract_prices(before)
        p_after = extract_prices(after)

        delta = {}
        for bk, aft in p_after.items():
            bef = p_before.get(bk, {})
            changes = {}
            for name, price in aft.items():
                prev = bef.get(name)
                if prev is None:
                    changes[name] = {"before": None, "after": price}
                elif prev != price:
                    changes[name] = {"before": prev, "after": price, "diff": price - prev}
            if changes:
                delta[bk] = changes

        return delta


if __name__ == "__main__":
    c = OddsAPIClient()
    try:
        sample = c.load_fixture("tests/fixtures/sample_odds.json")
        print("Loaded sample odds; bookmakers:", [b.get("key") for b in sample.get("bookmakers", [])])
    except FileNotFoundError:
        print("Add tests/fixtures/sample_odds.json for dry-run")
