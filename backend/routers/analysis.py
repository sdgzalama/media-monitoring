from fastapi import APIRouter, HTTPException
from database.connection import get_db
from nlp.ai_extractor import extract_analysis_from_ai
from nlp.theme_classifier import classify_into_thematic_areas

router = APIRouter(prefix="/process", tags=["AI Processing"])


@router.post("/media-item/{media_id}")
def process_media_item(media_id: str):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # 1. Fetch media item
    cursor.execute("SELECT * FROM media_items WHERE id = %s", (media_id,))
    item = cursor.fetchone()

    if not item:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Media item not found")

    # fallback if no body
    article_text = item["raw_text"] or item["raw_title"]

    # 2. Fetch ALL projects linked to this media item
    cursor.execute("""
        SELECT project_id 
        FROM project_media_items
        WHERE media_item_id = %s
    """, (media_id,))
    project_links = cursor.fetchall()

    if not project_links:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Media item is not assigned to any project")

    # Extract AI data once
    ai_output = extract_analysis_from_ai(article_text)

    if not ai_output:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail="AI extraction failed")

    # Guarantee fields
    for f in ["industry_name","industry_tactic","stakeholders","targeted_policy","geographical_focus","outcome_impact"]:
        ai_output.setdefault(f, "")

    stakeholders_str = (
        ", ".join(ai_output["stakeholders"])
        if isinstance(ai_output["stakeholders"], list)
        else str(ai_output["stakeholders"])
    )

    # 3. Update base AI extraction (same for all projects)
    cursor.execute("""
        UPDATE media_items SET
            industry_name=%s,
            industry_tactic=%s,
            stakeholders=%s,
            targeted_policy=%s,
            geographical_focus=%s,
            outcome_impact=%s,
            analysis_status='extracted'
        WHERE id=%s
    """, (
        ai_output["industry_name"],
        ai_output["industry_tactic"],
        stakeholders_str,
        ai_output["targeted_policy"],
        ai_output["geographical_focus"],
        ai_output["outcome_impact"],
        media_id
    ))

    # 4. Classify themes per project
    classified = {}

    for project in project_links:
        pid = project["project_id"]

        cursor.execute("""
            SELECT id, name, description
            FROM thematic_areas
            WHERE project_id = %s
        """, (pid,))
        areas = cursor.fetchall()

        theme_ids = classify_into_thematic_areas(article_text, areas)
        classified[pid] = theme_ids

        # Save in media item (combined list)
        # NOTE: This stores ALL project theme ids in one column. 
        # If you want project-specific storage, I can add a new table.
        all_ids = ",".join(theme_ids)

        cursor.execute("""
            UPDATE media_items
            SET semantic_area_ids = %s
            WHERE id = %s
        """, (
            all_ids,
            media_id
        ))

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "status": "success",
        "media_id": media_id,
        "ai_output": ai_output,
        "classified": classified
    }
