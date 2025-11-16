from fastapi import BackgroundTasks
from typing import List
import threading
import time

from routers.analysis import process_single_media_item
from database.connection import get_db

# GLOBAL PROGRESS TRACKER
progress = {
    "running": False,
    "total": 0,
    "done": 0
}


def _run_bulk(ids: List[str]):
    """Runs in a background thread."""
    progress["running"] = True
    progress["total"] = len(ids)
    progress["done"] = 0

    for media_id in ids:
        try:
            process_single_media_item(media_id)
        except Exception as e:
            print("AI ERROR processing", media_id, " → ", e)

        progress["done"] += 1
        time.sleep(0.2)  # Prevent CPU blocking

    progress["running"] = False


def queue_bulk_processing(background: BackgroundTasks, ids: List[str]):
    """Schedules background bulk processing."""
    background.add_task(_run_bulk, ids)
    return True


def get_progress():
    return progress
