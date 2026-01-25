# API Layer - bridge between HTTP requests and business logic
# Receives request, validates incoming data, calls business logic, returns response to user

from fastapi import APIRouter
from app.models.schemas import RewriteRequest, RewriteResponse, ValidationResponse
from app.services.rewriter import rewrite_bullets as rewrite_bullets_service

router = APIRouter(prefix="/api/bullets", tags=["bullets"])

@router.post("/rewrite", response_model=RewriteResponse)
async def rewrite_bullets(request: RewriteRequest): 
    return await rewrite_bullets_service(request.bullets, request.job_description)

@router.post("/validate", response_model=ValidationResponse)
async def validate_bullets(request: RewriteRequest):
    # Business logic to validate bullets would go here
    pass
    

