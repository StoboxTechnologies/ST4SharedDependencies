from http import HTTPStatus

import aioboto3
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from stobox_dependencies.settings.conf import Env
from stobox_dependencies.settings.conf import settings


class DynamicCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if settings.ENV == Env.TESTING:
            return await call_next(request)

        origin = request.headers.get('origin')
        allowed_origins = await self.get_allowed_origins()

        if origin and origin in allowed_origins:
            response = await call_next(request)
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Headers'] = 'Authorization,Content-Type'
            response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
            return response

        if request.method == 'OPTIONS':
            return Response(status_code=HTTPStatus.NO_CONTENT)

        return await call_next(request)

    @staticmethod
    async def get_allowed_origins() -> list[str]:
        session = aioboto3.Session(
            region_name=settings.AWS_DEFAULT_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        async with session.resource('dynamodb') as dynamodb:
            table = await dynamodb.Table(settings.ALLOWED_ORIGINS_TABLE_NAME)
            scan_response = await table.scan(AttributesToGet=['origin'])
            return [item['origin'] for item in scan_response.get('Items', [])]
