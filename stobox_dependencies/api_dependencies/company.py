from http import HTTPStatus

from fastapi import Depends
from fastapi import HTTPException

from stobox_dependencies.clients import company_client
from stobox_dependencies.schemes.company import Company
from stobox_dependencies.schemes.company import KYBState
from stobox_dependencies.settings.constants import ErrorMessages


async def get_company_info(company_id: int) -> Company:
    user_info = await company_client.get_company_info(company_id)
    return user_info


async def kyb_approved_company(company: Company = Depends(get_company_info)) -> None:
    if company.kyb_state == KYBState.APPROVED:
        return

    raise HTTPException(
        status_code=HTTPStatus.FORBIDDEN,
        detail=ErrorMessages.FORBIDDEN_ACCESS_KYC_STATE,
        headers={'WWW-Authenticate': 'Bearer'},
    )
