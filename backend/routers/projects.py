# backend/routers/projects.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from database.connection import get_db
import uuid

router = APIRouter(prefix="/projects", tags=["Projects"])

# -----------------------------
# Pydantic model for validation
# -----------------------------
class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    client_id: str

    category_ids: List[str] = []
    collaborator_ids: List[str] = []
    media_source_ids: List[str] = []
    report_avenue_ids: List[str] = []
    report_time_ids: List[str] = []
    report_consultation_ids: List[str] = []


# -----------------------------
# POST: Create new project
# -----------------------------
@router.post("/")
def create_project(project: ProjectCreate):
    project_id = str(uuid.uuid4())

    try:
        conn = get_db()
        cursor = conn.cursor()

        # ---------------------------------------
        # 1. Insert into projects table
        # ---------------------------------------
        sql_project = """
            INSERT INTO projects (id, title, description, client_id)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql_project, (
            project_id,
            project.title,
            project.description,
            project.client_id,
        ))

        # ---------------------------------------
        # Helper function for pivot tables
        # ---------------------------------------
        def insert_many_to_many(table, items, column_name):
            if items:
                sql = f"INSERT INTO {table} (project_id, {column_name}) VALUES (%s, %s)"
                cursor.executemany(sql, [(project_id, item) for item in items])

        # ---------------------------------------
        # 2. Insert many-to-many mappings
        # ---------------------------------------
        insert_many_to_many("project_categories", project.category_ids, "category_id")
        insert_many_to_many("project_collaborators", project.collaborator_ids, "collaborator_id")
        insert_many_to_many("project_media_sources", project.media_source_ids, "media_source_id")
        insert_many_to_many("project_report_avenues", project.report_avenue_ids, "report_avenue_id")
        insert_many_to_many("project_report_times", project.report_time_ids, "report_time_id")
        insert_many_to_many("project_report_consultations", project.report_consultation_ids, "report_consultation_id")

        conn.commit()

        # ---------------------------------------
        # Response
        # ---------------------------------------
        return {
            "status": "success",
            "message": "Project created successfully",
            "data": {
                "id": project_id,
                "title": project.title,
                "description": project.description,
                "client_id": project.client_id,
                "category_ids": project.category_ids,
                "collaborator_ids": project.collaborator_ids,
                "media_source_ids": project.media_source_ids,
                "report_time_ids": project.report_time_ids,
                "report_avenue_ids": project.report_avenue_ids,
                "report_consultation_ids": project.report_consultation_ids
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create project: {str(e)}"
        )

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
