# backend/routers/scrape.py

from fastapi import APIRouter, HTTPException, Query
from scrapers.rss_scraper import scrape_rss
from database.connection import get_db

router = APIRouter(prefix="/scrape", tags=["Scraping"])


@router.post("/rss")
def scrape_rss_endpoint(
    project_id: str = Query(...),
    source_id: str = Query(...)
):
    """
    Scrape ANY RSS feed using the URL stored in media_sources.base_url
    """
    # 1. Fetch RSS URL from DB
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT base_url, name
        FROM media_sources
        WHERE id = %s
    """, (source_id,))
    
    source = cursor.fetchone()
    cursor.close()
    conn.close()

    if not source:
        raise HTTPException(status_code=404, detail="Source ID not found")

    feed_url = source["base_url"]
    source_name = source["name"]

    if not feed_url:
        raise HTTPException(status_code=400, detail=f"No feed URL for {source_name}")

    # 2. Scrape RSS
    items = scrape_rss(project_id, source_id, feed_url)

    return {
        "status": "success",
        "source": source_name,
        "feed_url": feed_url,
        "total": len(items),
        "items": items
    }
