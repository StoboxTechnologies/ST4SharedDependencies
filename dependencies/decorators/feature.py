import functools

from fastapi import HTTPException
from starlette import status

from dependencies.clients import payment_client
from dependencies.settings.constants import ErrorMessages


def feature_validating(feature: str):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            user_id = kwargs.get('user_id')
            if user_id is None:
                raise ValueError('user_id must be provided as a keyword argument')

            response = await payment_client.is_feature_enables(user_id, feature)
            if not response.get('is_enabled', False):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=ErrorMessages.FEATURE_NOT_ENABLED.format(feature=feature),
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator
