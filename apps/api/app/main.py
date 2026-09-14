from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.user import router as user_router
from app.api.routes.workspace import router as workspace_router
from app.core.error_handlers import register_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import RequestLoggingMiddleware

configure_logging()

app = FastAPI(title="Enterprise Copilot API", version="0.1.0")
app.add_middleware(RequestLoggingMiddleware)
register_exception_handlers(app)

app.include_router(health_router)
app.include_router(user_router, prefix="/api/v1")
app.include_router(workspace_router, prefix="/api/v1")
