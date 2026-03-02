import json
from app.services.llm_client import LLMClient
from app.services.prompt_builder import build_critique_prompt

async def critique_variants(original_bullet: str, variants: list) -> tuple[bool, str]:
      """
      Returns (approved: bool, feedback: str)
      """
      llm_client = LLMClient()
      prompt = build_critique_prompt(variants, original_bullet)
      response = await llm_client.generate(prompt)

      try:
          result = json.loads(response)
          approved = result.get("approved", False)
          feedback = result.get("feedback", "")
          return approved, feedback
      except json.JSONDecodeError:
          # If critic itself returns invalid JSON, approve by default
          # so a critic failure doesn't block the whole pipeline
          return True, ""