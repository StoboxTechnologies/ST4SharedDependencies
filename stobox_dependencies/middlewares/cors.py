from starlette.middleware.cors import ALL_METHODS
from starlette.middleware.cors import CORSMiddleware

from stobox_dependencies.clients.dynamo import dynamo_client


class DynamicCORSMiddleware(CORSMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allow_methods = kwargs.get('allow_methods', ALL_METHODS)

    async def __call__(self, *args, **kwargs):
        self.allow_origins = await dynamo_client.get_cors_domains()
        return await super().__call__(*args, **kwargs)
