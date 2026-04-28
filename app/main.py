from fastapi import FastAPI
from app.api.routes import router as notify_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(notify_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
