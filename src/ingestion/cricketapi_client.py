import os
import json
import requests
from typing import Dict, Any, Optional


class CricketAPIClient:
    """Minimal client for CricketAPI / Roanuz Cricket data.

    This is a stateless wrapper: it does not persist data. If `api_key` is not
    provided, the client can load a local JSON fixture via `fixture_path` for
    development and testing.
    """

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://www.cricketapi.com/v5"):
        self.api_key = api_key or os.getenv("CRICKETAPI_KEY")
        self.base_url = base_url.rstrip("/")

    def _get(self, path: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        params = params or {}
        if self.api_key:
            params.setdefault("api_key", self.api_key)
        url = f"{self.base_url}/{path.lstrip('/') }"
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()

    def load_fixture(self, fixture_path: str) -> Dict[str, Any]:
        with open(fixture_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_match(self, match_key: str, fixture_path: Optional[str] = None) -> Dict[str, Any]:
        """Return a normalized match snapshot.

        If `fixture_path` is provided and no API key is set, the fixture will be
        loaded instead of calling the remote API.
        """
        if fixture_path and not self.api_key:
            raw = self.load_fixture(fixture_path)
        else:
            raw = self._get(f"docs/match-rest-api/{match_key}")

        # Normalization: build compact snapshot used by pipeline
        return self._normalize_match(raw)

    def _normalize_match(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        # Raw docs vary by provider. Try to extract common fields safely.
        m = {}
        m["match_id"] = raw.get("match_id") or raw.get("id") or raw.get("key")
        m["status"] = raw.get("status") or raw.get("match_status")
        m["teams"] = {
            "home": raw.get("home_team") or raw.get("teams", [None, None])[0],
            "away": raw.get("away_team") or raw.get("teams", [None, None])[1],
        }
        # score/overs
        score = raw.get("score") or raw.get("scores") or {}
        m["score"] = score

        # ball-by-ball (if available)
        m["balls"] = raw.get("ball_by_ball") or raw.get("ball_by_ball_updates") or raw.get("ball_by_ball_events") or raw.get("balls") or []

        # current over / batsmen / bowler
        m["current_over"] = raw.get("over") or raw.get("current_over")
        m["batsmen"] = raw.get("batsmen") or raw.get("batting") or []
        m["bowler"] = raw.get("bowler") or raw.get("bowling") or None

        return m


if __name__ == "__main__":
    # quick smoke test using fixtures if present
    client = CricketAPIClient()
    try:
        sample = client.load_fixture("tests/fixtures/sample_match.json")
        print(client._normalize_match(sample))
    except FileNotFoundError:
        print("No fixture found. Provide CRICKETAPI_KEY or add tests/fixtures/sample_match.json")
