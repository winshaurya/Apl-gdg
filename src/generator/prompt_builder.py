from typing import Dict, Any


def build_prompt(match_state: Dict[str, Any], odds_delta: Dict[str, Any], twitter_signals: Dict[str, Any]) -> str:
    """Create a prompt for the generative model to produce a dramatic 3-over script.

    The prompt is intentionally structured but kept short so an LLM can expand.
    """
    teams = match_state.get("teams", {})
    score = match_state.get("score")
    current_over = match_state.get("current_over")

    lines = []
    lines.append(f"Match snapshot: {teams.get('home')} vs {teams.get('away')}")
    if score:
        lines.append(f"Current score: {score}")
    if current_over is not None:
        lines.append(f"Current over: {current_over}")

    # Odds summary
    if odds_delta:
        lines.append("Recent betting odds shifts:")
        for bk, changes in list(odds_delta.items())[:3]:
            lines.append(f"- {bk}: {changes}")

    # Twitter summary
    if twitter_signals.get("top_hashtags"):
        hs = ", ".join([h for h, _ in twitter_signals["top_hashtags"][:5]])
        lines.append(f"Twitter trending: {hs}")

    lines.append("")
    lines.append('Task: Write a vivid, dramatic 3-over "script" predicting key events (wickets, boundaries, talking-points) for the next three overs. Integrate the betting-odds shifts and Twitter drama so the script feels plausible. Label the output clearly as fiction and do not encourage betting.')
    lines.append("Format: short play-by-play lines per ball with a one-paragraph teaser headline.")

    return "\n".join(lines)
