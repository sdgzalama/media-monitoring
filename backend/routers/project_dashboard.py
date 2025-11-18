from fastapi import APIRouter, HTTPException
from database.connection import get_db

router = APIRouter(prefix="/project", tags=["Project Dashboard"])


@router.get("/{project_id}/dashboard")
def project_dashboard(project_id: str):

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # --------------------------------
        # 1. VALIDATE PROJECT
        # --------------------------------
        cursor.execute("""
            SELECT 
                p.id,
                p.title,
                p.description,
                c.name AS client_name
            FROM projects p
            LEFT JOIN clients c ON p.client_id = c.id
            WHERE p.id = %s
        """, (project_id,))
        project = cursor.fetchone()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # --------------------------------
        # 2. BASE COUNTS
        # --------------------------------
        cursor.execute("""
            SELECT 
                COUNT(*) AS total_items,
                SUM(CASE WHEN m.analysis_status='extracted' THEN 1 ELSE 0 END) AS extracted_items,
                SUM(CASE WHEN m.analysis_status='raw' THEN 1 ELSE 0 END) AS awaiting_items
            FROM media_items m
            JOIN project_media_items pmi ON pmi.media_item_id = m.id
            WHERE pmi.project_id = %s
        """, (project_id,))
        stats = cursor.fetchone()

        # --------------------------------
        # 3. BY SOURCE
        # --------------------------------
        cursor.execute("""
            SELECT s.name, COUNT(*) AS count
            FROM media_items m
            JOIN project_media_items pmi ON pmi.media_item_id = m.id
            JOIN media_sources s ON m.source_id = s.id
            WHERE pmi.project_id = %s
            GROUP BY s.name
            ORDER BY count DESC
        """, (project_id,))
        by_source = cursor.fetchall()

        # --------------------------------
        # 4. THEMATIC AREA DISTRIBUTION
        # --------------------------------
        cursor.execute("""
            SELECT t.name, COUNT(*) AS count
            FROM media_items m
            JOIN project_media_items pmi ON pmi.media_item_id = m.id
            JOIN thematic_areas t
                ON FIND_IN_SET(t.id, m.semantic_area_ids)
            WHERE pmi.project_id = %s
            GROUP BY t.name
            ORDER BY count DESC
        """, (project_id,))
        themes = cursor.fetchall()

        # --------------------------------
        # 5. INDUSTRY NAMES
        # --------------------------------
        cursor.execute("""
            SELECT industry_name, COUNT(*) AS count
            FROM media_items m
            JOIN project_media_items pmi ON pmi.media_item_id = m.id
            WHERE pmi.project_id = %s
            AND industry_name IS NOT NULL AND industry_name != ''
            GROUP BY industry_name
            ORDER BY count DESC
        """, (project_id,))
        industry_names = cursor.fetchall()

        # --------------------------------
        # 6. INDUSTRY TACTICS
        # --------------------------------
        cursor.execute("""
            SELECT industry_tactic, COUNT(*) AS count
            FROM media_items m
            JOIN project_media_items pmi ON pmi.media_item_id = m.id
            WHERE pmi.project_id = %s
            AND industry_tactic IS NOT NULL AND industry_tactic != ''
            GROUP BY industry_tactic
            ORDER BY count DESC
        """, (project_id,))
        tactics = cursor.fetchall()

        # --------------------------------
        # 7. STAKEHOLDERS
        # --------------------------------
        cursor.execute("""
            SELECT stakeholders
            FROM media_items m
            JOIN project_media_items pmi ON pmi.media_item_id = m.id
            WHERE pmi.project_id = %s
            AND stakeholders IS NOT NULL AND stakeholders != ''
        """, (project_id,))
        rows = cursor.fetchall()

        stakeholder_count = {}
        for row in rows:
            names = [n.strip() for n in row["stakeholders"].split(",")]
            for n in names:
                if n:
                    stakeholder_count[n] = stakeholder_count.get(n, 0) + 1

        # --------------------------------
        # 8. GEO FOCUS
        # --------------------------------
        cursor.execute("""
            SELECT geographical_focus, COUNT(*) AS count
            FROM media_items m
            JOIN project_media_items pmi ON pmi.media_item_id = m.id
            WHERE pmi.project_id = %s
            AND geographical_focus IS NOT NULL AND geographical_focus != ''
            GROUP BY geographical_focus
            ORDER BY count DESC
        """, (project_id,))
        geo = cursor.fetchall()

        # --------------------------------
        # 9. OUTCOMES
        # --------------------------------
        cursor.execute("""
            SELECT outcome_impact, COUNT(*) AS count
            FROM media_items m
            JOIN project_media_items pmi ON pmi.media_item_id = m.id
            WHERE pmi.project_id = %s
            AND outcome_impact IS NOT NULL AND outcome_impact != ''
            GROUP BY outcome_impact
            ORDER BY count DESC
        """, (project_id,))
        outcomes = cursor.fetchall()

        return {
            "project": project,
            "stats": stats,
            "sources": by_source,
            "themes": themes,
            "industry_names": industry_names,
            "tactics": tactics,
            "stakeholders": stakeholder_count,
            "geographical_focus": geo,
            "outcomes": outcomes
        }

    finally:
        if cursor: cursor.close()
        if conn: conn.close()
