from stobox_dependencies.clients.aws import AWSClient
from stobox_dependencies.settings.conf import settings


class DynamoClient(AWSClient):
    CLIENT_TYPE = 'dynamodb'
    IS_RESOURCE_CLIENT = True

    async def add_cors_domain(self, domain: str) -> None:
        table = await self.client.Table(settings.ALLOWED_ORIGINS_TABLE_NAME)
        await table.put_item(
            TableName=settings.ALLOWED_ORIGINS_TABLE_NAME,
            Item={'origin': domain},
        )

    async def get_cors_domains(self) -> list[str]:
        table = await self.client.Table(settings.ALLOWED_ORIGINS_TABLE_NAME)
        scan_response = await table.scan(AttributesToGet=['origin'])
        return [item['origin'] for item in scan_response.get('Items', [])]

dynamo_client = DynamoClient()
