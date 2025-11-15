# backend/nlp/semantic_generator.py

import uuid
from database.connection import get_db

def generate_semantic_areas(project_id: str, title: str, description: str):
    """
    Temporary dummy generator.
    Replace with real AI when API key is available.
    """

    thematic_list = [
        {"name": "Industry Interference", "description": "Actions by industries to influence policy."},
        {"name": "Policy Manipulation", "description": "Attempts to shift regulations and guidelines."},
        {"name": "Public Narratives", "description": "Messaging used to influence public opinion."},
        {"name": "Regulatory Frameworks", "description": "Laws, institutions, and procedures involved."},
        {"name": "Advocacy and Influence", "description": "Actors pushing certain political or economic agendas."}
    ]

    conn = get_db()
    cursor = conn.cursor()

    sql = """
        INSERT INTO thematic_areas (id, project_id, name, description)
        VALUES (%s, %s, %s, %s)
    """

    inserted = []

    for item in thematic_list:
        theme_id = str(uuid.uuid4())
        cursor.execute(sql, (
            theme_id,
            project_id,
            item["name"],
            item["description"]
        ))
        inserted.append({
            "id": theme_id,
            "name": item["name"],
            "description": item["description"]
        })

    conn.commit()
    cursor.close()
    conn.close()

    return inserted
