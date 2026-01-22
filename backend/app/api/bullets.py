# API Layer - bridge between HTTP requests and business logic
# Receives request, validates incoming data, calls business logic, returns response to user

from fastapi import APIRouter
from app.models.schemas import RewriteRequest, RewriteResponse, ValidationResponse

router = APIRouter(prefix="/api/bullets", tags=["bullets"])

@router.post("/rewrite", response_model=RewriteResponse)
async def rewrite_bullets(request: RewriteRequest): 
    # Business logic to rewrite bullets would go here
    pass

@router.post("/validate", response_model=ValidationResponse)
async def validate_bullets(request: RewriteRequest):
    # Business logic to validate bullets would go here
    pass
    

