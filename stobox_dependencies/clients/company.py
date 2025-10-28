from stobox_dependencies.clients.http import BaseHTTPClient
from stobox_dependencies.schemes.company import Company


class CompanyHTTPClient(BaseHTTPClient):
    class ROUTES:
        PUBLIC_COMPANY_INFO: str = '/companies/{company_id}/public'
        TOKEN_INFO_BY_ADDRESS: str = 'internal/tokens/by-address/{address}'

    async def get_public_company_info(self, company_id: int) -> Company:
        response = await self.get(url=self.ROUTES.PUBLIC_COMPANY_INFO.format(company_id=company_id))
        return Company.model_validate(response.json())


    async def get_token_info_by_address(self, address: str) -> TokenSchema:
        response = await self.get(url=self.ROUTES.TOKEN_INFO_BY_ADDRESS.format(address=address))
        return TokenSchema.model_validate(response.json())
