import logging
from http import HTTPStatus

from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse

from dependencies.exceptions import AuthError
from dependencies.exceptions import DoesNotExistError
from dependencies.exceptions import HTTPClientError
from dependencies.exceptions import ValidationError

logger = logging.getLogger(__name__)


def http_client_exception_handler(request: Request, exc: HTTPClientError) -> Response:
    logger.error(
        {
            'message': str(exc),
            'user_id': getattr(request.state, 'user_id', None),
        }
    )
    return JSONResponse(
        status_code=HTTPStatus.BAD_GATEWAY,
        content=HTTPStatus.BAD_GATEWAY.phrase,
    )


async def does_not_exist_exception_handler(request: Request, exc: DoesNotExistError) -> Response:
    return await http_exception_handler(
        request=request,
        exc=HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(exc)),
    )


async def unauthorized_exception_handler(request: Request, exc: AuthError) -> Response:
    return await http_exception_handler(
        request=request,
        exc=HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=str(exc)),
    )


async def validation_exception_handler(request: Request, exc: ValidationError) -> Response:
    return await http_exception_handler(
        request=request,
        exc=HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(exc)),
    )
