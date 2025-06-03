import boto3
from starlette.middleware.cors import ALL_METHODS
from starlette.middleware.cors import CORSMiddleware

from stobox_dependencies.settings.conf import settings


class DynamicCORSMiddleware(CORSMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allow_origins = self.get_allowed_origins()
        self.allow_methods = kwargs.get('allow_methods', ALL_METHODS)

    @staticmethod
    def get_dynamodb_table():
        session = boto3.Session(
            region_name=settings.AWS_DEFAULT_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        dynamodb = session.resource('dynamodb')
        return dynamodb.Table(settings.ALLOWED_ORIGINS_TABLE_NAME)

    @classmethod
    def get_allowed_origins(cls) -> list[str]:
        table = cls.get_dynamodb_table()
        scan_response = table.scan(AttributesToGet=['origin'])
        return [item['origin'] for item in scan_response.get('Items', [])]

    @classmethod
    def set_allowed_origins(cls, allowed_origins: list[str]):
        table = cls.get_dynamodb_table()
        with table.batch_writer() as batch:
            for origin in allowed_origins:
                batch.put_item(Item={'origin': origin})
