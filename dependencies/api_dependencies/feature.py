from http import HTTPStatus

from fastapi import Depends
from fastapi import HTTPException

from dependencies.api_dependencies.auth import current_user_id
from dependencies.clients import payment_client
from dependencies.settings.constants import ErrorMessages


async def feature_enabled(
    feature: str,
    user_id: int = Depends(current_user_id),
) -> None:
    response = await payment_client.is_feature_enables(user_id, feature)
    if not response.get('is_enabled', False):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=ErrorMessages.FEATURE_NOT_ENABLED.format(feature=feature),
            headers={'WWW-Authenticate': 'Bearer'},
        )
