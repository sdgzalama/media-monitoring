from fastapi import APIRouter, HTTPException
from database.connection import get_db
from nlp.ai_extractor import extract_analysis_from_ai
from nlp.theme_classifier import classify_into_thematic_areas
import json

router = APIRouter(prefix="/process", tags=["AI Processing"])


@router.post("/media-item/{media_id}")
def process_single_media_item(media_id: str):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # -------------------------
    # 1. Fetch media item
    # -------------------------
    cursor.execute("SELECT * FROM media_items WHERE id = %s", (media_id,))
    item = cursor.fetchone()

    if not item:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Media item not found")

    # Fallback: If raw_text is short or empty, use raw_title
    article_text = item["raw_text"]
    if not article_text or len(article_text.strip()) < 50:
        article_text = item["raw_title"]

    # -------------------------
    # 2. Fetch thematic areas (NEW)
    # -------------------------
    cursor.execute("""
        SELECT id, name, description
        FROM thematic_areas
        WHERE project_id = %s
    """, (item["project_id"],))
    thematic_areas = cursor.fetchall()

    # -------------------------
    # 3. Run AI extraction
    # -------------------------
    ai_output = extract_analysis_from_ai(article_text)

    if ai_output is None or not isinstance(ai_output, dict):
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=500,
            detail="AI extraction failed — Invalid JSON output"
        )

    # Guarantee required fields exist
    for field in [
        "industry_name", "industry_tactic", "stakeholders",
        "targeted_policy", "geographical_focus", "outcome_impact"
    ]:
        ai_output.setdefault(field, "")

    # Convert stakeholders list → comma-separated string
    stakeholders_str = (
        ", ".join(ai_output["stakeholders"])
        if isinstance(ai_output.get("stakeholders"), list)
        else str(ai_output.get("stakeholders", ""))
    )

    # -------------------------
    # 4. AI THEMATIC CLASSIFICATION (NEW)
    # -------------------------
    try:
        theme_ids = classify_into_thematic_areas(article_text, thematic_areas)
    except Exception as e:
        print("THEME CLASSIFICATION ERROR:", e)
        theme_ids = []

    semantic_ids_str = ",".join(theme_ids) if theme_ids else ""

    # -------------------------
    # 5. Update media item
    # -------------------------
    update_sql = """
        UPDATE media_items SET
            industry_name = %s,
            industry_tactic = %s,
            stakeholders = %s,
            targeted_policy = %s,
            geographical_focus = %s,
            outcome_impact = %s,
            semantic_area_ids = %s,
            analysis_status = 'extracted'
        WHERE id = %s
    """

    cursor.execute(update_sql, (
        ai_output.get("industry_name", ""),
        ai_output.get("industry_tactic", ""),
        stakeholders_str,
        ai_output.get("targeted_policy", ""),
        ai_output.get("geographical_focus", ""),
        ai_output.get("outcome_impact", ""),
        semantic_ids_str,    # NOW SAVING THEMATIC AREAS
        media_id
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "status": "success",
        "media_id": media_id,
        "analysis": ai_output,
        "classified_themes": theme_ids
    }


# @router.post("/media-item/process-all")
# def process_all_items():
#     conn = get_db()
#     cursor = conn.cursor(dictionary=True)

#     cursor.execute("SELECT id FROM media_items WHERE analysis_status = 'raw'")
#     items = cursor.fetchall()

#     processed = []

#     for item in items:
#         try:
#             process_single_media_item(item["id"])
#             processed.append(item["id"])
#         except Exception as e:
#             print("Error processing item:", item["id"], e)

#     return {
#         "status": "success",
#         "processed_count": len(processed),
#         "processed_ids": processed
#     }
