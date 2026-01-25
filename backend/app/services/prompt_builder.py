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

    STRICT RULES:
1. NEVER invent metrics, numbers, percentages, or statistics
2. If the original has no numbers, your rewrite must have no numbers
3. Use qualitative language instead (e.g., "improved", "enhanced", "streamlined")
4. Ask follow-up questions to get the real metrics

    If a target job description is provided, tailor the bullet point to emphasize skills and 
    experiences relevant to that job.

    IMPORTANT: Do NOT invent or hallucinate metrics, numbers, or statistics that were not in the original bullet. 
    If the original bullet lacks specific metrics, keep the rewrite qualitative and add follow-up questions asking for the missing details.

    If the bullet point is missing quantified metrics (numbers, percentages, dollar amounts),
    add follow-up questions asking for specific details that would strengthen the bullet point.

    Remember: NO INVENTED NUMBERS. If unsure, keep it qualitative.
    
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