from fastapi import Depends
from fastapi import Header
from pydantic import ValidationError

from stobox_dependencies.api_dependencies.auth import current_user_id
from stobox_dependencies.api_dependencies.auth import get_access_token
from stobox_dependencies.clients import user_client
from stobox_dependencies.exceptions import HTTPClientError
from stobox_dependencies.settings.constants import ErrorMessages


async def validate_otp(
    secret_otp: str = Header(),
    token: str = Depends(get_access_token),
) -> None:
    try:
        await user_client.verify_otp(token, secret_otp)
    except HTTPClientError:
        raise ValidationError(ErrorMessages.INVALID_OTP)


async def validate_2fa(
    secret_2fa: str | None = Header(None),
    user_id: int = Depends(current_user_id),
    token: str = Depends(get_access_token),
) -> None:
    try:
        user_info = await user_client.get_user_info(user_id)
    except HTTPClientError:
        raise ValidationError(ErrorMessages.INVALID_2FA)

    if not user_info.is_2fa_enabled:
        return

    if secret_2fa is None:
        raise ValidationError(ErrorMessages.INVALID_2FA)

    try:
        await user_client.verify_2fa(token, secret_2fa)
    except HTTPClientError:
        raise ValidationError(ErrorMessages.INVALID_2FA)
