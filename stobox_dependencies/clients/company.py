from stobox_dependencies.clients.http import BaseHTTPClient
from stobox_dependencies.schemes.company import Company
from stobox_dependencies.settings.conf import settings


class CompanyHTTPClient(BaseHTTPClient):
    BASE_URL = settings.COMPANY_MANAGER_URL

    class ROUTES:
        COMPANY_INFO: str = '/{company_id}/public'

    async def get_company_info(self, company_id: int) -> Company:
        response = await self.get(url=self.ROUTES.COMPANY_INFO.format(company_ref=company_id))
        return Company.model_validate(response.json())
