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
        # cursor.execute("SELECT * FROM projects WHERE id = %s", (project_id,))
        # project = cursor.fetchone()
        cursor.execute("""
            SELECT 
                p.id,
                p.title,
                p.description,
                p.client_id,
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
                SUM(CASE WHEN analysis_status='extracted' THEN 1 ELSE 0 END) AS extracted_items,
                SUM(CASE WHEN analysis_status='raw' THEN 1 ELSE 0 END) AS awaiting_items
            FROM media_items
            WHERE project_id = %s
        """, (project_id,))
        base_counts = cursor.fetchone()

        # --------------------------------
        # 3. MEDIA SOURCE DISTRIBUTION
        # --------------------------------
        cursor.execute("""
            SELECT s.name, COUNT(*) AS count
            FROM media_items m
            JOIN media_sources s ON m.source_id = s.id
            WHERE m.project_id = %s
            GROUP BY s.name
            ORDER BY count DESC
        """, (project_id,))
        by_source = cursor.fetchall()

        # --------------------------------
        # 4. THEMATIC AREA DISTRIBUTION
        # --------------------------------
        cursor.execute("""
            SELECT 
                t.name,
                COUNT(*) AS count
            FROM media_items m
            JOIN thematic_areas t 
                ON FIND_IN_SET(t.id, m.semantic_area_ids)
            WHERE m.project_id = %s
            GROUP BY t.name
            ORDER BY count DESC
        """, (project_id,))
        theme_distribution = cursor.fetchall()

        # --------------------------------
        # 5. INDUSTRY NAME FREQUENCY
        # --------------------------------
        cursor.execute("""
            SELECT industry_name, COUNT(*) AS count
            FROM media_items
            WHERE project_id = %s
            AND industry_name IS NOT NULL AND industry_name != ''
            GROUP BY industry_name
            ORDER BY count DESC
        """, (project_id,))
        industry_names = cursor.fetchall()

        # --------------------------------
        # 6. INDUSTRY TACTICS FREQUENCY
        # --------------------------------
        cursor.execute("""
            SELECT industry_tactic, COUNT(*) AS count
            FROM media_items
            WHERE project_id = %s
            AND industry_tactic IS NOT NULL AND industry_tactic != ''
            GROUP BY industry_tactic
            ORDER BY count DESC
        """, (project_id,))
        tactics = cursor.fetchall()

        # --------------------------------
        # 7. STAKEHOLDER FREQUENCY
        # --------------------------------
        cursor.execute("""
            SELECT stakeholders
            FROM media_items
            WHERE project_id = %s
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
        # 8. GEOGRAPHICAL FOCUS
        # --------------------------------
        cursor.execute("""
            SELECT geographical_focus, COUNT(*) AS count
            FROM media_items
            WHERE project_id = %s
            AND geographical_focus IS NOT NULL AND geographical_focus != ''
            GROUP BY geographical_focus
            ORDER BY count DESC
        """, (project_id,))
        geo_focus = cursor.fetchall()

        # --------------------------------
        # 9. OUTCOME / IMPACT
        # --------------------------------
        cursor.execute("""
            SELECT outcome_impact, COUNT(*) AS count
            FROM media_items
            WHERE project_id = %s
            AND outcome_impact IS NOT NULL AND outcome_impact != ''
            GROUP BY outcome_impact
            ORDER BY count DESC
        """, (project_id,))
        outcomes = cursor.fetchall()

        return {
            "project": project,
            "stats": base_counts,
            "sources": by_source,
            "themes": theme_distribution,
            "industry_names": industry_names,
            "tactics": tactics,
            "stakeholders": stakeholder_count,
            "geographical_focus": geo_focus,
            "outcomes": outcomes
        }

    finally:
        if cursor: cursor.close()
        if conn: conn.close()
