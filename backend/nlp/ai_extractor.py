import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load .env properly
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),   # ✅ FIXED
    base_url="https://openrouter.ai/api/v1"
)

def extract_analysis_from_ai(text: str):
    prompt = f"""
    Analyze this media article and extract:

    - industry_name
    - industry_tactic
    - stakeholders
    - targeted_policy
    - geographical_focus
    - outcome_impact

    Respond in CLEAN JSON ONLY with this structure:

    {{
      "industry_name": "",
      "industry_tactic": "",
      "stakeholders": [],
      "targeted_policy": "",
      "geographical_focus": "",
      "outcome_impact": ""
    }}

    Article:
    {text}
    """

    try:
        response = client.chat.completions.create(
            model="google/gemma-3-4b-it:free",
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response.choices[0].message.content.strip()

        # Remove Markdown wrappers if present
        if raw.startswith("```"):
            raw = raw.split("```")[1].replace("json", "").strip()

        return json.loads(raw)

    except Exception as e:
        print("\n🔥 REAL AI ERROR BELOW 🔥")
        print(type(e))
        print(str(e))
        print("-----------------------------------------------------\n")
        return None
