from fastapi import FastAPI

app = FastAPI(
    title="QC Workflow System",
    version="1.0.0",
)

@app.get("/health")
def health_check():
    return {"status": "ok"}
