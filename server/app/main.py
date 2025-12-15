from fastapi import FastAPI
from app.api.drawings import router as drawings_router

app = FastAPI(
    title="QC Workflow System",
    version="1.0.0",
)

app.include_router(drawings_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
