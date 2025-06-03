import aioboto3
from starlette.middleware.cors import ALL_METHODS
from starlette.middleware.cors import CORSMiddleware

from stobox_dependencies.settings.conf import settings


class DynamicCORSMiddleware(CORSMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allow_origins = self.get_allowed_origins()
        self.allow_methods = kwargs.get('allow_methods', ALL_METHODS)

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

    @staticmethod
    async def set_allowed_origins(allowed_origins: list[str]):
        session = aioboto3.Session(
            region_name=settings.AWS_DEFAULT_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        async with session.resource('dynamodb') as dynamodb:
            table = await dynamodb.Table(settings.ALLOWED_ORIGINS_TABLE_NAME)
            for origin in allowed_origins:
                await table.put_item(Item={'origin': origin})
