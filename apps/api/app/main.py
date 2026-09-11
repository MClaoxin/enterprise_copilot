from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.user import router as user_router

app = FastAPI(title = "Enterprise Copilot API", version = "0.1.0")

app.include_router(health_router)
app.include_router(user_router, prefix="/api/v1")