from http import HTTPStatus
from typing import Any

from fastapi import Depends
from fastapi import HTTPException

from stobox_dependencies.api_dependencies.auth import current_user_id
from stobox_dependencies.api_dependencies.auth import validate_access_token
from stobox_dependencies.clients import user_client
from stobox_dependencies.schemes.user import ACTIVE_USER_STATUSES
from stobox_dependencies.schemes.user import User
from stobox_dependencies.schemes.user import UserFractalState
from stobox_dependencies.schemes.user import UserKYCState
from stobox_dependencies.settings.constants import ErrorMessages


async def active_user(token_payload: dict[str, Any] = Depends(validate_access_token)) -> None:
    if token_payload.get('status') not in ACTIVE_USER_STATUSES:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=ErrorMessages.FORBIDDEN_ACCESS_INACTIVE_USER,
            headers={'WWW-Authenticate': 'Bearer'},
        )


async def get_user_info(user_id: int = Depends(current_user_id)) -> User:
    user_info = await user_client.get_user_info(user_id)
    return user_info


async def kyc_approved_user(user: User = Depends(get_user_info)) -> None:
    if user.kyc_state == UserKYCState.APPROVED or user.fractal_state == UserFractalState.APPROVED:
        return

    raise HTTPException(
        status_code=HTTPStatus.FORBIDDEN,
        detail=ErrorMessages.FORBIDDEN_ACCESS_KYC_STATE,
        headers={'WWW-Authenticate': 'Bearer'},
    )
