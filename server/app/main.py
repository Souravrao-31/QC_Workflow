from fastapi import FastAPI
from app.api.drawings import router as drawings_router
from app.api.auth import router as auth_router
from app.api.admin_users import router as admin_users_router


app = FastAPI(
    title="QC Workflow System",
    version="1.0.0",
)

app.include_router(drawings_router)
app.include_router(auth_router)
app.include_router(admin_users_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}



