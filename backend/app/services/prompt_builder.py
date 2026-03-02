import json

def build_rewrite_prompt(bullet: str, job_description: str = None, feedback: str = None) -> str:
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
    else:
        job_context = "No job description provided. Write general-purpose improvements."

    prompt = f"""You are a resume expert. Rewrite the following resume bullet point into three variants:
    - impact_first: Lead with the measurable result or outcome 
    - scope_first: Lead with scale, team size, or project scope.
    If no scope information exists in the original bullet, ask a follow-up
    question instead of inventing one, and write the variant without scope.
    - tech_first: Lead with technologies, tools, or methodologies used.
    If the original bullet mentions NO specific technologies, do NOT name any tools.
    Instead write a generic variant and add a follow-up question asking which tools were used.

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
    
   {f"Feedback from previous attempt: {feedback}. Make sure your rewrite addresses this feedback." if feedback else ""}

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

def build_correction_prompt(invalid_response: str) -> str:
    correction_prompt = f"""Your previous response was not valid JSON.
                    Here was your response: {invalid_response}

                    Please return ONLY valid JSON with this exact structure:
                    {{
                    "variants": [
                        {{"variant_type": "impact_first", "text": "your rewritten bullet here"}},
                        {{"variant_type": "scope_first", "text": "your rewritten bullet here"}},
                        {{"variant_type": "tech_first", "text": "your rewritten bullet here"}}
                    ],
                    "follow_up_questions": []
                    }}
    """
    return correction_prompt

def build_critique_prompt(variants: list, original_bullet: str) -> str:
  return f"""You are a strict resume critic. Evaluate each variant ONLY against its own specific rule.

  Original bullet: "{original_bullet}"

  Variants:
  {json.dumps(variants, indent=2)}

  Evaluate each variant independently:

  - impact_first: Does it lead with an outcome or result? Reject if it leads with a task or action instead.
  - scope_first: Does it lead with scale, team size, or project scope? Reject if it leads with anything else.
  - tech_first: Does it lead with a specific technology, tool, or methodology? Reject if it leads with anything
  else.

  Global rules that apply to ALL variants:
  - No variant may contain metrics or numbers not present in the original bullet
  - If the original bullet contains no technology names or tool names, the tech_first variant must not name any specific tools, languages, or software. If it does, reject it.
  - If the original bullet contains no scope details, the scope_first variant must not invent team sizes, platforms, or scale. If it does, reject it.

  Respond with valid JSON only:
  {{
    "approved": true or false,
    "feedback": "specific explanation referencing the variant_type and which rule it broke, or empty string if
  approved"
  }}
  """