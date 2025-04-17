from http import HTTPStatus
from typing import Any

from fastapi import Depends
from fastapi import HTTPException

from dependencies.api_dependencies.auth import current_user_id
from dependencies.api_dependencies.auth import validate_access_token
from dependencies.clients import user_client
from dependencies.schemes.user import ACTIVE_USER_STATUSES
from dependencies.schemes.user import UserKYCState
from dependencies.settings.constants import ErrorMessages


async def active_user(token_payload: dict[str, Any] = Depends(validate_access_token)) -> None:
    if token_payload.get('status') not in ACTIVE_USER_STATUSES:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=ErrorMessages.FORBIDDEN_ACCESS_INACTIVE_USER,
            headers={'WWW-Authenticate': 'Bearer'},
        )


async def kyc_approved_user(user_id: int = Depends(current_user_id)) -> None:
    user_info = await user_client.get_user_info(user_id)
    if user_info.kyc_state != UserKYCState.APPROVED:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=ErrorMessages.FORBIDDEN_ACCESS_KYC_STATE,
            headers={'WWW-Authenticate': 'Bearer'},
        )
