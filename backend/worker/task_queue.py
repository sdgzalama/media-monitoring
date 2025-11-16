from fastapi import BackgroundTasks
from routers.analysis import process_single_media_item

def queue_bulk_processing(background: BackgroundTasks, item_ids: list):
    for media_id in item_ids:
        background.add_task(process_single_media_item, media_id)
