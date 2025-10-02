from http import HTTPStatus

from fastapi import Depends
from fastapi import HTTPException

from stobox_dependencies.api_dependencies.auth import current_user_id
from stobox_dependencies.clients import payment_client
from stobox_dependencies.schemes.payment_center import UserFeatureConsumeSchema
from stobox_dependencies.settings.constants import ErrorMessages


class FeatureEnabled:
    def __init__(self, feature: str):
        self.feature = feature

    async def __call__(self, user_id: int = Depends(current_user_id)):
        response = await payment_client.is_feature_enables(user_id, self.feature)
        if not response.get('is_enabled', False):
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail=ErrorMessages.FEATURE_NOT_ENABLED.format(feature=self.feature),
                headers={'WWW-Authenticate': 'Bearer'},
            )


class FeatureConsume:
    def __init__(self, feature: str):
        self.feature = feature

    async def __call__(self, user_id: int = Depends(current_user_id)):
        await FeatureEnabled(self.feature)(user_id)

        yield

        consume_feature_data = UserFeatureConsumeSchema(
            user_id=user_id,
            feature_name=self.feature,
        )
        await payment_client.consume_user_feature(consume_feature_data)
