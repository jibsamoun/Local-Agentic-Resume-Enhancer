from app.services.llm_client import LLMClient
from app.services.prompt_builder import build_rewrite_prompt, build_correction_prompt
from app.services.validator import validate_bullet
from app.models.schemas import RewriteResponse, BulletRewrite, RewriteVariant, ValidationResponse
import json

def parse_llm_response(raw: str, bullet: str, validation: ValidationResponse) -> BulletRewrite:
    response_data = json.loads(raw)

    variants = [
        RewriteVariant(variant_type=v["variant_type"], text=v["text"])
        for v in response_data.get("variants", [])
    ]

    follow_up_questions = []
    for q in response_data.get("follow_up_questions", []):
        if isinstance(q, str):
            follow_up_questions.append(q)
        elif isinstance(q, dict) and "question" in q:
            follow_up_questions.append(q["question"])

    return BulletRewrite(
        original_bullet=bullet,
        variants=variants,
        follow_up_questions=follow_up_questions,
        validation=validation
    )

async def rewrite_bullets(bullets: list[str], job_description: str = None, max_retries: int = 3) -> RewriteResponse:
    llm_client = LLMClient()
    results = []

    for bullet in bullets:
        validation_response = validate_bullet(bullet)
        validation = ValidationResponse(
            warnings=validation_response.warnings,
            errors=validation_response.errors
        )

        prompt = build_rewrite_prompt(bullet, job_description)
        llm_response = await llm_client.generate(prompt)

        for attempt in range(max_retries):
            try:
                bullet_rewrite = parse_llm_response(llm_response, bullet, validation)
                break  # Success — exit retry loop
            except json.JSONDecodeError:
                if attempt == max_retries - 1:
                    print(f"All {max_retries} attempts failed. Returning empty result.")
                    bullet_rewrite = BulletRewrite(
                        original_bullet=bullet,
                        variants=[],
                        follow_up_questions=["LLM returned invalid response after all retries. Please try again."],
                        validation=validation
                    )
                else:
                    print(f"Attempt {attempt + 1} failed. Retrying...")
                    correction_prompt = build_correction_prompt(llm_response)
                    llm_response = await llm_client.generate(correction_prompt)

        results.append(bullet_rewrite)

    return RewriteResponse(results=results)