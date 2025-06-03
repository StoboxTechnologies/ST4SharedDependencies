import boto3
from starlette.middleware.cors import CORSMiddleware
from starlette.types import Receive
from starlette.types import Scope
from starlette.types import Send

from stobox_dependencies.settings.conf import settings


class DynamicCORSMiddleware(CORSMiddleware):
    def __init__(self, *args, **kwargs):
        self.dynamo_table = self.get_dynamodb_table()
        super().__init__(*args, **kwargs)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        self.allow_origins = self.get_allowed_origins()
        await super().__call__(scope, receive, send)

    @staticmethod
    def get_dynamodb_table():
        session = boto3.Session(
            region_name=settings.AWS_DEFAULT_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        dynamodb = session.resource('dynamodb')
        return dynamodb.Table(settings.ALLOWED_ORIGINS_TABLE_NAME)

    def get_allowed_origins(self) -> list[str]:
        scan_response = self.dynamo_table.scan(AttributesToGet=['origin'])
        return [item['origin'] for item in scan_response.get('Items', [])]

    def set_allowed_origins(self, allowed_origins: list[str]):
        with self.dynamo_table.batch_writer() as batch:
            for origin in allowed_origins:
                batch.put_item(Item={'origin': origin})
