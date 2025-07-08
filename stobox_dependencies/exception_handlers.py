import logging
from http import HTTPStatus

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from fastapi.responses import Response

from stobox_dependencies.exceptions import AuthError
from stobox_dependencies.exceptions import DoesNotExistError
from stobox_dependencies.exceptions import ForbiddenError
from stobox_dependencies.exceptions import HTTPClientError
from stobox_dependencies.exceptions import ValidationDetailedError
from stobox_dependencies.exceptions import ValidationError

logger = logging.getLogger(__name__)


class FastAPIExceptionHandlers:
    def __init__(self, app: FastAPI):
        self.app = app
        self.register_default_handlers()
        self.register_handlers()

    def register_default_handlers(self):
        self.app.exception_handler(HTTPClientError)(self.http_client_exception_handler)
        self.app.exception_handler(DoesNotExistError)(self.does_not_exist_exception_handler)
        self.app.exception_handler(ValidationError)(self.validation_exception_handler)
        self.app.exception_handler(ValidationDetailedError)(self.validation_exception_handler_with_detail)
        self.app.exception_handler(ForbiddenError)(self.forbidden_exception_handler)
        self.app.exception_handler(AuthError)(self.auth_exception_handler)

    def register_handlers(self):
        """Override this method in subclasses to register additional exception handlers."""
        pass

    async def http_client_exception_handler(self, request: Request, exc: HTTPClientError) -> Response:
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

    async def does_not_exist_exception_handler(self, request: Request, exc: DoesNotExistError) -> Response:
        return await http_exception_handler(
            request=request,
            exc=HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(exc)),
        )

    async def forbidden_exception_handler(self, request: Request, exc: ForbiddenError) -> Response:
        return await http_exception_handler(
            request=request,
            exc=HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(exc)),
        )

    async def auth_exception_handler(self, request: Request, exc: AuthError) -> Response:
        return await http_exception_handler(
            request=request,
            exc=HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=str(exc)),
        )

    async def validation_exception_handler(self, request: Request, exc: ValidationError) -> Response:
        return await http_exception_handler(
            request=request,
            exc=HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(exc)),
        )

    async def validation_exception_handler_with_detail(
        self,
        request: Request,
        exc: ValidationDetailedError,
    ) -> Response:
        detail = exc.args[0] if exc.args else str(exc)
        return await http_exception_handler(
            request=request,
            exc=HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=detail),
        )
