import os
import requests
import json
from sentence_transformers import SentenceTransformer, util

# Load embeddings model once
embedder = SentenceTransformer("all-MiniLM-L6-v2")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"


# ---------------------------------------------------------
# OPTIONAL: LLM relevance confirmation (final step)
# ---------------------------------------------------------
def llm_relevancy_check(title, description, article):
    question = f"""
Project Title: {title}
Project Description: {description}

Article Title: {article["raw_title"]}
Article Body: {article["raw_text"][:800]}

Question:
Is this article related to the project? 
Answer STRICTLY with: "YES" or "NO"
"""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    payload = {
        "model": "deepseek-v2",
        "messages": [
            {"role": "system", "content": "You classify article relevance."},
            {"role": "user", "content": question}
        ],
        "temperature": 0.0
    }

    try:
        res = requests.post(DEEPSEEK_URL, json=payload, headers=headers)
        ans = res.json()["choices"][0]["message"]["content"].strip().upper()
        return "YES" in ans
    except:
        return True   # fallback


# ---------------------------------------------------------
# BALANCED R2 RELEVANCE FILTERING
# ---------------------------------------------------------
def filter_relevant_articles(project_title, project_desc, articles):
    # 1. Build project embedding
    project_text = project_title + " " + project_desc
    proj_embed = embedder.encode(project_text, convert_to_tensor=True)

    relevant = []

    for article in articles:
        # 2. quick skip if article has no text
        if not article["raw_text"]:
            continue

        full_text = article["raw_title"] + " " + article["raw_text"]

        # 3. embedding similarity (Balanced threshold = 0.38)
        art_embed = embedder.encode(full_text, convert_to_tensor=True)
        sim_score = float(util.cos_sim(proj_embed, art_embed)[0])

        if sim_score < 0.38:
            continue

        # 4. keyword match from project title
        key = project_title.lower()
        if key not in full_text.lower():
            # acceptable, but check deeper
            pass

        # 5. LLM confirmation (Balanced R2)
        if not llm_relevancy_check(project_title, project_desc, article):
            continue

        relevant.append(article)

    return relevant
