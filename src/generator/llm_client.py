import os
from typing import Optional


class LLMClient:
    """Simple LLM wrapper. By default returns a deterministic stub unless
    `OPENAI_API_KEY` is provided and `openai` is installed.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        try:
            import openai
            self.openai = openai
        except Exception:
            self.openai = None

    def generate(self, prompt: str, max_tokens: int = 512) -> str:
        if self.openai and self.api_key:
            self.openai.api_key = self.api_key
            resp = self.openai.ChatCompletion.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.9,
            )
            return resp["choices"][0]["message"]["content"]

        # Fallback deterministic stub for offline development
        teaser = "[FICTION] Teaser: A sudden twist of fate flips the match narrative."
        body = []
        body.append(teaser)
        body.append("Over 1: 6 balls — tight bowling, a couple of nervy singles, one edge dropped.")
        body.append("Over 2: 6 balls — two boundaries, a dramatic run-out, crowd gasps.")
        body.append("Over 3: 6 balls — a late overburst: one huge six, one wicket.")
        body.append("Note: This is a fictional script integrating imaginary odds movement and social chatter. Do not take as real betting advice.")
        return "\n".join(body)
