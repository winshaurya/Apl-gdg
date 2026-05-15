import os
import google.genai as genai


# -----------------------------
# CONFIGURE GEMINI (ONCE)
# -----------------------------
def configure_gemini():
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("❌ GOOGLE_API_KEY not set. Run: export GOOGLE_API_KEY=your_key")

    genai.configure(api_key=api_key)


# -----------------------------
# GENERATE INSIGHTS
# -----------------------------
def generate_insights(context: str):

    try:
        configure_gemini()

        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(context)

        # Safe extraction
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        else:
            return "⚠️ No valid response from Gemini"

    except Exception as e:
        print("⚠️ Gemini failed:", str(e))
        return "AI insights unavailable"