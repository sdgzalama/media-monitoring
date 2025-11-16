# items.py
# from fastapi import APIRouter

# router = APIRouter(prefix="/items", tags=["Media Items"])

# @router.get("/")
# def get_items():
#     return {"message": "List of media items"}

from fastapi import APIRouter, HTTPException
from database.connection import get_db
# from routers.analysis import process_single_media_item   # IMPORT THIS


processing_progress = {
    "total": 0,
    "done": 0,
    "running": False
}

router = APIRouter(prefix="/media", tags=["Media Items"])

# ---------------------------------------------
# EXISTING MEDIA ITEMS ENDPOINTS (yours)
# ---------------------------------------------
# Example:
# @router.get("/")
# def list_media_items(): ...

# ---------------------------------------------
# NEW: LATEST 10 MEDIA ITEMS
# ---------------------------------------------
# @router.post("/process/all")
# def process_all_items():
#     conn = get_db()
#     cursor = conn.cursor(dictionary=True)

#     cursor.execute("SELECT id FROM media_items WHERE analysis_status = 'raw'")
#     items = cursor.fetchall()

#     # FIX: dynamic import to avoid circular dependency
#     from routers.analysis import process_single_media_item as process_ai

#     for item in items:
#         process_ai(item["id"])

#     cursor.close()
#     conn.close()

#     return {"status": "processing_started", "count": len(items)}

from fastapi import APIRouter, BackgroundTasks
from database.connection import get_db
from worker.task_queue import queue_bulk_processing

router = APIRouter(prefix="/media", tags=["Media Items"])

@router.post("/process/all")
def process_all_items(background: BackgroundTasks):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id FROM media_items WHERE analysis_status = 'raw'")
    items = cursor.fetchall()

    ids = [row["id"] for row in items]

    queue_bulk_processing(background, ids)

    cursor.close()
    conn.close()

    return {
        "status": "queued",
        "total": len(ids),
        "message": "Processing started in background"
    }


@router.get("/latest/10")
def latest_media_items():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT 
        m.id,
        LEFT(m.raw_text, 60) AS title,
        m.analysis_status,
        s.name AS media_source_name
    FROM media_items m
    JOIN media_sources s ON m.source_id = s.id
    ORDER BY m.scraped_at DESC
    LIMIT 10
""")

    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items


# ---------------------------------------------
# NEW: PROCESS ALL AWAITING MEDIA ITEMS
# ---------------------------------------------
# @router.post("/process/all")
# def process_all_items():
#     global processing_progress

#     conn = None
#     cursor = None

#     try:
#         conn = get_db()
#         cursor = conn.cursor(dictionary=True)

#         cursor.execute("SELECT id FROM media_items WHERE analysis_status = 'raw'")
#         items = cursor.fetchall()

#         # Set progress initial state
#         processing_progress = {
#             "total": len(items),
#             "done": 0,
#             "running": True
#         }

#         for item in items:
#             try:
#                 process_single_media_item(item["id"])
#                 processing_progress["done"] += 1
#             except Exception as e:
#                 print("PROCESS ERROR:", e)
#                 continue

#         processing_progress["running"] = False

#         return {
#             "status": "ok",
#             "processed": processing_progress["done"]
#         }

#     finally:
#         if cursor: cursor.close()
#         if conn: conn.close()


@router.get("/progress")
def get_processing_progress():
    return processing_progress
