import os
import json
from typing import Dict, Any, List, Optional

try:
    import tweepy
except Exception:
    tweepy = None


class TwitterClient:
    """Minimal Twitter/X client. Uses `tweepy` if available.

    If no credentials are provided, the client can load a local fixture for
    development and testing.
    """

    def __init__(self, bearer_token: Optional[str] = None):
        self.bearer_token = bearer_token or os.getenv("TWITTER_BEARER_TOKEN")
        self.client = None
        if tweepy and self.bearer_token:
            self.client = tweepy.Client(bearer_token=self.bearer_token, wait_on_rate_limit=True)

    def load_fixture(self, fixture_path: str) -> Dict[str, Any]:
        with open(fixture_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_trends_for_match(self, match_keywords: List[str], fixture_path: Optional[str] = None) -> Dict[str, Any]:
        """Return aggregated trending hashtags/tweet counts related to `match_keywords`.

        If `fixture_path` provided and no bearer token set, load fixture instead.
        """
        if fixture_path and not self.client:
            return self.load_fixture(fixture_path)

        if not self.client:
            # fallback empty structure
            return {"top_hashtags": [], "top_tweets": []}

        # perform recent search for each keyword and aggregate simple stats
        query = " OR ".join(match_keywords)
        resp = self.client.search_recent_tweets(query=query, max_results=50, tweet_fields=["public_metrics","created_at"], expansions=None)
        tweets = resp.data or []
        hashtags = {}
        for t in tweets:
            text = t.text
            for token in text.split():
                if token.startswith("#"):
                    hashtags[token.lower()] = hashtags.get(token.lower(), 0) + 1

        top_hashtags = sorted(hashtags.items(), key=lambda x: -x[1])[:10]
        top_tweets = [t.text for t in tweets[:10]]
        return {"top_hashtags": top_hashtags, "top_tweets": top_tweets}


if __name__ == "__main__":
    tc = TwitterClient()
    print(tc.get_trends_for_match(["#IPL", "#IPL2026"]))
