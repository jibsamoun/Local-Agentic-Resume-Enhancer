# What to say to Ollama
def build_rewrite_prompt(bullet: str, job_description: str = None) -> str:
    """
    Builds a prompt to rewrite a resume bullet point.

    Args:
        bullet (str): The original resume bullet point.
        job_description (str, optional): The job description to tailor the bullet point to.

    Returns:
        str: The constructed prompt.
    """
    
    job_context = ""
    if job_description:
        job_context = f"Target job description: {job_description}"

    prompt = f"""You are a resume expert. Rewrite the following resume bullet point into three variants:
    - impact_first: Lead with the measurable result or outcome 
    - scope_first: Lead with scale, team size, or project scope
    - tech_first: Lead with the technologies, tools, or methodologies used

    If a target job description is provided, tailor the bullet point to emphasize skills and 
    experiences relevant to that job.

    If the bullet point is missing quantified metrics (numbers, percentages, dollar amounts),
    add follow-up questions asking for specific details that would strengthen the bullet point.

    Original bullet point: {bullet}
    {job_context}
    Respond with valid JSON only, no other text:
    {{
      "variants": [
        {{
          "variant_type": "impact_first",
          "text": "your rewritten bullet here"
        }},
        {{
          "variant_type": "scope_first",
          "text": "your rewritten bullet here"
        }},
        {{
          "variant_type": "tech_first",
          "text": "your rewritten bullet here"
        }}
      ],
      "follow_up_questions": []
    }}"""

    return prompt