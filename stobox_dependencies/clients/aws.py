import contextlib
import logging
from typing import TYPE_CHECKING

import aioboto3

from stobox_dependencies.exceptions import AWSClientError
from stobox_dependencies.settings.conf import settings

if TYPE_CHECKING:
    from aiobotocore.client import AioBaseClient

logger = logging.getLogger(__name__)


class AWSClient:
    CLIENT_TYPE: str
    IS_RESOURCE_CLIENT: bool = False

    def __init__(self):
        self._client = None
        self._context_stack = contextlib.AsyncExitStack()
        self.session = aioboto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    @property
    def client(self) -> 'AioBaseClient':
        if not self._client:
            raise AWSClientError(f'AWS {self.CLIENT_TYPE.upper()} client not configured')
        return self._client

    async def configure(self, region: str = settings.AWS_DEFAULT_REGION):
        if self.IS_RESOURCE_CLIENT:
            self._client = await self._context_stack.enter_async_context(
                self.session.resource(self.CLIENT_TYPE, region_name=region)
            )
        else:
            self._client = await self._context_stack.enter_async_context(
                self.session.client(self.CLIENT_TYPE, region_name=region)
            )
        logger.info({'message': f'AWS {self.CLIENT_TYPE.upper()} client has been configured.'})

    async def close(self):
        await self._context_stack.aclose()
