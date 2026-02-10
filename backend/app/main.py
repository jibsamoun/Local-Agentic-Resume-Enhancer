from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.bullets import router as bullets_router

app = FastAPI(
    title="Local Agentic Resume Enhancer",
    version="0.1.0",
)

# Allow frontend to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


# TODO: Mount bullet routes from app.api.bullets
app.include_router(bullets_router)
