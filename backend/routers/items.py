from fastapi import APIRouter, BackgroundTasks
from database.connection import get_db
from worker.task_queue import queue_bulk_processing, get_progress

router = APIRouter(prefix="/media", tags=["Media Items"])

# 1. GET — list media items
@router.get("/")
def list_media_items():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            m.id,
            m.raw_title,
            LEFT(m.raw_text, 120) AS preview,
            m.url AS url,
            m.analysis_status,
            m.scraped_at,
            s.name AS source_name
        FROM media_items m
        LEFT JOIN media_sources s ON m.source_id = s.id
        ORDER BY m.scraped_at DESC
    """)

    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items


# 2. POST — process all RAW items in background
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


# 3. GET — latest 10 items
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


# 4. GET — processing progress
@router.get("/progress")
def get_processing_progress():
    return get_progress()
