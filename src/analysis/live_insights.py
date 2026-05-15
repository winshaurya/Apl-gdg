def generate_live_match_insights(match_name):

    print(f"\n🚀 Generating LIVE insights for: {match_name}")

    # Simulated Gemini-style input (replace later with API)
    summary = f"""
Match: {match_name}

RCB scored 198/5 in 20 overs.
Kohli scored 82(54).
SRH chased with strong middle overs but fell short by 12 runs.
"""

    print("\n🧠 Match Summary:")
    print(summary)

    # Simple insights (rule-based)
    insights = []

    if "198" in summary:
        insights.append("High scoring match — batting-friendly pitch.")

    if "middle overs" in summary:
        insights.append("Middle overs were decisive phase.")

    if "fell short" in summary:
        insights.append("Chasing pressure impacted outcome.")

    print("\n🔥 Insights:")
    for i, ins in enumerate(insights, 1):
        print(f"{i}. {ins}")

    print("\n✅ LIVE ANALYSIS COMPLETE\n")