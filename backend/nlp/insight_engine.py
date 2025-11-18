import uuid
import json
import os
from datetime import datetime
from database.connection import get_db
from nlp.relevance_filter import filter_relevant_articles
import requests

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"


# ---------------------------------------------------------
# DEEPSEEK AI REQUEST
# ---------------------------------------------------------
def deepseek_json(messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    payload = {
        "model": "deepseek-v2",
        "messages": messages,
        "temperature": 0.3,
        "response_format": { "type": "json_object" }
    }

    res = requests.post(DEEPSEEK_URL, json=payload, headers=headers)

    if res.status_code != 200:
        raise Exception(f"DeepSeek Error: {res.text}")

    data = res.json()
    content = data["choices"][0]["message"]["content"]

    return json.loads(content)


# ---------------------------------------------------------
# MAIN INSIGHT GENERATOR (STRUCTURED)
# ---------------------------------------------------------
def generate_project_insights(project_id: str):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # 1. Get project details
    cursor.execute("""
        SELECT title, description
        FROM projects
        WHERE id = %s
    """, (project_id,))
    project = cursor.fetchone()

    if not project:
        cursor.close()
        conn.close()
        return None

    title = project["title"]
    description = project.get("description") or ""

    # 2. Load articles for the project
    cursor.execute("""
        SELECT raw_title, raw_text
        FROM media_items m
        JOIN project_media_items pmi ON pmi.media_item_id = m.id
        WHERE pmi.project_id = %s
    """, (project_id,))
    articles = cursor.fetchall()

    if not articles:
        cursor.close()
        conn.close()
        return None

    # 3. FILTER articles using balanced engine (R2)
    relevant_articles = filter_relevant_articles(title, description, articles)

    if len(relevant_articles) == 0:
        insight_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO project_insights (id, project_id, relevance_count)
            VALUES (%s, %s, %s)
        """, (insight_id, project_id, 0))
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "no_relevant_articles"}

    # 4. Build text block
    media_block = "\n\n".join(
        f"TITLE: {a['raw_title']}\nBODY: {a['raw_text']}"
        for a in relevant_articles
    )

    # 5. DeepSeek JSON Prompt
    prompt = f"""
Analyze the following media coverage for a project called "{title}":

Project Description:
{description}

Media Articles:
{media_block}

Return analysis ONLY as valid JSON with these fields:

{{
  "executive_summary": "",
  "topic_clusters": [],
  "subthemes": [],
  "sentiment": {{
      "positive": 0,
      "negative": 0,
      "neutral": 0
  }},
  "entities": {{
      "people": [],
      "organizations": [],
      "locations": []
  }},
  "narratives": "",
  "issue_forecast": "",
  "risk_scoring": {{
      "score": 0,
      "explanation": ""
  }},
  "opportunity_scoring": {{
      "score": 0,
      "explanation": ""
  }},
  "recommendations": "",
  "deep_context": "",
  "engagement_predictions": ""
}}
"""

    messages = [
        {"role": "system", "content": "You are a media intelligence system."},
        {"role": "user", "content": prompt}
    ]

    analysis = deepseek_json(messages)

    # 6. Save to database (structured)
    insight_id = str(uuid.uuid4())

    cursor.execute("""
        INSERT INTO project_insights (
            id, project_id, generated_at, relevance_count,
            executive_summary, topic_clusters, subthemes, sentiment,
            entities, narratives, issue_forecast, risk_scoring,
            opportunity_scoring, recommendations, deep_context,
            engagement_predictions
        ) VALUES (%s, %s, NOW(), %s,
                  %s, %s, %s, %s,
                  %s, %s, %s, %s,
                  %s, %s, %s, %s)
    """, (
        insight_id,
        project_id,
        len(relevant_articles),
        analysis["executive_summary"],
        json.dumps(analysis["topic_clusters"]),
        json.dumps(analysis["subthemes"]),
        json.dumps(analysis["sentiment"]),
        json.dumps(analysis["entities"]),
        analysis["narratives"],
        analysis["issue_forecast"],
        json.dumps(analysis["risk_scoring"]),
        json.dumps(analysis["opportunity_scoring"]),
        analysis["recommendations"],
        analysis["deep_context"],
        analysis["engagement_predictions"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "status": "ok",
        "insight_id": insight_id,
        "articles_used": len(relevant_articles)
    }
