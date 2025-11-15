def extract_industry_info(text, url, project_semantics):
    prompt = f"""
    You are an expert media analyst.

    Based on the following text, extract the structured information in this JSON format:

    {{
      "date": "",
      "industry_name": "",
      "industry_tactic": "",
      "description": "",
      "stakeholders": "",
      "targeted_policy": "",
      "geographical_focus": "",
      "outcome_impact": "",
      "source": "{url}",
      "semantic_categories": []
    }}

    Use the client's defined semantic area list:
    {project_semantics}

    If details are not available, leave blank but keep keys.
    
    TEXT:
    {text}
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.choices[0].message["content"])
