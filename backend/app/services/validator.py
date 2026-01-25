# Validates input data for correct business logic processing
from app.models.schemas import ValidationResponse

ACTION_VERBS = ["led", "managed", "developed", "designed", "implemented", "created", "improved", "optimized", "analyzed", "coordinated", "executed", "produced", "increased", "decreased", "streamlined", "facilitated", "collaborated", "initiated", "spearheaded", "orchestrated", "engineered"]

FIRST_PERSON_PATTERNS = ["I ", "my ", "me ", "we ", "our ", "us "]

MAX_LENGTH = 150

def check_action_verb(bullet: str) -> bool:
    words = bullet.split(maxsplit=1)
    first_word = words[0].lower()
    return first_word in ACTION_VERBS

def check_first_person(bullet: str) -> bool:
    bullet_lower = bullet.lower()
    for word in FIRST_PERSON_PATTERNS:
        if word.lower() in bullet_lower:
            return True
    return False

def check_length(bullet: str) -> bool:
    return len(bullet) > MAX_LENGTH

def check_metrics(bullet: str) -> bool:
    if any(char.isdigit() for char in bullet):
        return True
    return False

def validate_bullet(bullet: str) -> ValidationResponse:
    response = ValidationResponse()

    if not check_action_verb(bullet):
        response.errors.append("Bullet point should start with a strong action verb.")

    if check_first_person(bullet):
        response.errors.append("Bullet point should not contain first-person language.")

    if check_length(bullet):
        response.warnings.append("Bullet point exceeds 150 characters.")

    if not check_metrics(bullet):
        response.warnings.append("Consider adding quantified metrics to strengthen the bullet point.")

    return response