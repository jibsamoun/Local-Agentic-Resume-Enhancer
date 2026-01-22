from fastapi import FastAPI
from app.api.bullets import router as bullets_router

app = FastAPI(
    title="Local Agentic Resume Enhancer",
    version="0.1.0",
)


@app.get("/health")
async def health():
    return {"status": "ok"}


# TODO: Mount bullet routes from app.api.bullets
app.include_router(bullets_router)
