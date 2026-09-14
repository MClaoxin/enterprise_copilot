import logging
from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException

logger = logging.getLogger(__name__)


def _error_response(
    request: Request,
    status_code: int,
    code: str,
    message: str,
    details: object | None = None,
) -> JSONResponse:
    error: dict[str, object] = {"code": code, "message": message}
    if details is not None:
        error["details"] = jsonable_encoder(details)
    request_id = getattr(request.state, "request_id", None)
    response = JSONResponse(
        status_code=status_code,
        content={
            "error": error,
            "request_id": request_id,
        },
    )
    if request_id:
        response.headers["X-Request-ID"] = request_id
    return response


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    logger.warning(
        "Application error: code=%s status=%d path=%s",
        exc.code,
        exc.status_code,
        request.url.path,
    )
    return _error_response(request, exc.status_code, exc.code, exc.message)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    logger.warning("Request validation failed: path=%s", request.url.path)
    return _error_response(
        request,
        422,
        "VALIDATION_ERROR",
        "Request validation failed",
        exc.errors(),
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    message = (
        exc.detail
        if isinstance(exc.detail, str)
        else HTTPStatus(exc.status_code).phrase
    )
    return _error_response(request, exc.status_code, "HTTP_ERROR", message, exc.detail)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # The request middleware records the traceback while its request context is active.
    logger.error("Returning internal server error: path=%s", request.url.path)
    return _error_response(
        request,
        500,
        "INTERNAL_SERVER_ERROR",
        "An unexpected error occurred",
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
