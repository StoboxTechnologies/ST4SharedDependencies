from stobox_dependencies.clients.http import BaseHTTPClient
from stobox_dependencies.schemes.public_page import PublicPageInfo
from stobox_dependencies.settings.conf import settings


class PublicPageHTTPClient(BaseHTTPClient):
    BASE_URL = settings.PUBLIC_PAGE_URL

    class ROUTES:
        PUBLIC_PAGE_INFO: str = '/public-pages/public/{domain}'

    async def get_public_page_info(self, domain: str) -> PublicPageInfo:
        response = await self.get(url=self.ROUTES.PUBLIC_PAGE_INFO.format(domain=domain))
        return PublicPageInfo.model_validate(response.json())
