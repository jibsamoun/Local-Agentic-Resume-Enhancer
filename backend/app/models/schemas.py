from pydantic import BaseModel
from typing import Literal, Optional
VariantType = Literal["impact_first", "scope_first", "tech_first"]

class RewriteRequest(BaseModel):
    bullets: list[str]
    job_description: Optional[str]

class RewriteVariant(BaseModel):
    variant_type: VariantType
    text: str

class ValidationResponse(BaseModel):
    warnings: list[str] = []
    errors: list[str] = []
    
class BulletRewrite(BaseModel):
    original_bullet: str
    variants: list[RewriteVariant]
    follow_up_questions: list[str] = []
    validation: Optional[ValidationResponse] = None 

class RewriteResponse(BaseModel):
    results: list[BulletRewrite]
