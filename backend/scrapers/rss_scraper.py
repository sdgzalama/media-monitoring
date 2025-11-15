# backend/scrapers/rss_scraper.py

import uuid
import feedparser
import requests
from bs4 import BeautifulSoup
from database.connection import get_db
from datetime import datetime


RSS_FEEDS = {}


# -----------------------------------------
# FLEXIBLE FULL ARTICLE TEXT FETCHER
# -----------------------------------------
def fetch_article_text(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Try to extract article body
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
# SAVE ITEM TO DB
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
# FLEXIBLE RSS SCRAPER (WORKS FOR ANY FEED)
# -----------------------------------------
def scrape_rss(project_id: str, source_id: str, feed_url: str):
    print("Scraping RSS:", feed_url)

    feed = feedparser.parse(feed_url)

    # If feed is empty or invalid — return 0 items
    if not feed.entries:
        return []

    scraped_items = []

    for entry in feed.entries:
        title = entry.get("title", "")
        url = entry.get("link", "")

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

        scraped_items.append({
            "media_id": media_id,
            "title": title,
            "url": url,
            "published_at": published
        })

    return scraped_items
