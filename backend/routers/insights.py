from fastapi import APIRouter, HTTPException
from database.connection import get_db
from uuid import uuid4
from datetime import datetime

from nlp.insight_engine import generate_project_insights  # <- AI engine

router = APIRouter(prefix="/project", tags=["Insights"])


# ----------------------------------------------------------
# 1️⃣ GET LATEST INSIGHTS
# ----------------------------------------------------------
@router.get("/{project_id}/insights/latest")
def get_latest_insights(project_id: str):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM project_insights
        WHERE project_id = %s
        ORDER BY generated_at DESC
        LIMIT 1
    """, (project_id,))

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        return {"status": "empty"}

    # Convert JSON fields
    for key in ["topic_clusters", "subthemes", "sentiment", "entities",
                "risk_scoring", "opportunity_scoring"]:
        if key in row and isinstance(row[key], str):
            try:
                import json
                row[key] = json.loads(row[key])
            except:
                row[key] = None

    return row


# ----------------------------------------------------------
# 2️⃣ MANUAL TRIGGER — GENERATE INSIGHTS ON DEMAND
# ----------------------------------------------------------
@router.post("/{project_id}/insights/generate")
def generate_insights_now(project_id: str):

    try:
        new_id = generate_project_insights(project_id)
        return {"status": "success", "insight_id": new_id}

    except Exception as e:
        print("Insight generation failed:", e)
        raise HTTPException(status_code=500, detail="Insight generation failed")
