from fastapi import APIRouter
from database.connection import get_db

router = APIRouter(prefix="/media-sources", tags=["Media Sources"])

@router.get("/")
def list_sources():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, name FROM media_sources")
    sources = cursor.fetchall()

    cursor.close()
    conn.close()
    return sources
