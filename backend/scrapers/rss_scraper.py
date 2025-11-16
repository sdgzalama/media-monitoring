import uuid
import feedparser
import requests
from bs4 import BeautifulSoup
from database.connection import get_db
from datetime import datetime


# -----------------------------------------
# GET FULL ARTICLE TEXT
# -----------------------------------------
def fetch_article_text(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        article = soup.find("article")
        if article:
            paragraphs = article.find_all("p")
        else:
            paragraphs = soup.find_all("p")

        text = " ".join([p.get_text(strip=True) for p in paragraphs])
        return text.strip()
    except Exception as e:
        print("Article fetch failed:", e)
        return ""


# -----------------------------------------
# CHECK IF URL ALREADY EXISTS
# -----------------------------------------
def item_exists(url: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM media_items WHERE url = %s LIMIT 1", (url,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row is not None


# -----------------------------------------
# SAVE NEW MEDIA ITEM
# -----------------------------------------
def save_media_item(project_id, source_id, title, text, url, published_at):
    conn = get_db()
    cursor = conn.cursor()

    media_id = str(uuid.uuid4())

    sql = """
        INSERT INTO media_items (
            id, project_id, source_id,
            raw_title, raw_text, url,
            published_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (
        media_id,
        project_id,
        source_id,
        title,
        text,
        url,
        published_at
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return media_id


# -----------------------------------------
# SMART SCRAPER — inserts ONLY new items
# -----------------------------------------
def scrape_rss(project_id: str, source_id: str, feed_url: str):
    print("Scraping RSS:", feed_url)

    feed = feedparser.parse(feed_url)
    if not feed.entries:
        return {"new_items": 0, "skipped": 0, "items": []}

    inserted = 0
    skipped = 0
    results = []

    for entry in feed.entries:
        title = entry.get("title", "")
        url = entry.get("link", "")

        if not url:
            continue   # No URL means cannot track duplicates

        # --------- SKIP IF ALREADY SCRAPED ---------
        if item_exists(url):
            skipped += 1
            continue

        # Published date
        published = None
        if entry.get("published_parsed"):
            published = datetime(*entry.published_parsed[:6])

        # Fetch article body
        text = fetch_article_text(url)

        # Save to DB
        media_id = save_media_item(
            project_id, source_id, title, text, url, published
        )

        inserted += 1
        results.append({
            "media_id": media_id,
            "title": title,
            "url": url,
            "published_at": published
        })

    return {
        "new_items": inserted,
        "skipped": skipped,
        "items": results
    }
