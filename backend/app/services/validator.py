# Validates input data for correct business logic processing
import re
from app.models.schemas import ValidationResponse
from app.services.constants import ACTION_VERBS, FIRST_PERSON_PATTERNS, MAX_LENGTH


def normalize_bullet(bullet: str) -> str:
    """Strip whitespace, bullet symbols, and normalize for checking."""
    # Remove leading/trailing whitespace
    bullet = bullet.strip()
    # Remove common bullet symbols at the start
    bullet = re.sub(r'^[\•\-\*\>\—\–\·\○\●\■\□\➤\→]+\s*', '', bullet)
    return bullet


def extract_first_word(bullet: str) -> str:
    """Extract first word, stripping punctuation."""
    bullet = normalize_bullet(bullet)
    if not bullet:
        return ""
    words = bullet.split(maxsplit=1)
    if not words:
        return ""
    # Remove trailing punctuation from first word
    first_word = re.sub(r'[^\w]', '', words[0].lower())
    return first_word


def check_action_verb(bullet: str) -> bool:
    first_word = extract_first_word(bullet)
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