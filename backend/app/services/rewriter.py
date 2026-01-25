from app.services.llm_client import LLMClient
from app.services.prompt_builder import build_rewrite_prompt
from app.services.validator import validate_bullet
from app.models.schemas import RewriteResponse, BulletRewrite, RewriteVariant, ValidationResponse
import json

async def rewrite_bullets(bullets: list[str], job_description: str = None) -> RewriteResponse:
    llm_client = LLMClient()
    results = []

    for bullet in bullets:
        # Validate original bullet
        validation_response = validate_bullet(bullet)
        validation = ValidationResponse(
            warnings=validation_response.warnings,
            errors=validation_response.errors
        )

        # Build prompt
        prompt = build_rewrite_prompt(bullet, job_description)
        # Call LLM
        llm_client_response = await llm_client.generate(prompt)
        
        # Parse JSON Response
        try:
            response_data = json.loads(llm_client_response)
            
            # Success: create variants from response
            variants = [
                RewriteVariant(variant_type=variant["variant_type"], text=variant["text"])
                for variant in response_data.get("variants", [])
            ]

            # Handle follow_up_questions as strings or objects
            raw_questions = response_data.get("follow_up_questions", [])
            follow_up_questions = []
            for q in raw_questions:
                if isinstance(q, str):
                    follow_up_questions.append(q)
                elif isinstance(q, dict) and "question" in q:
                    follow_up_questions.append(q["question"])
            
            bullet_rewrite = BulletRewrite(
                original_bullet=bullet,
                variants=variants,
                follow_up_questions=follow_up_questions,
                validation=validation
            )
            
        except json.JSONDecodeError:
            # Failure: return empty result with error message
            bullet_rewrite = BulletRewrite(
                original_bullet=bullet,
                variants=[],
                follow_up_questions=["LLM returned invalid response. Please try again."],
                validation=validation
            )
        
        results.append(bullet_rewrite)

    return RewriteResponse(results=results)