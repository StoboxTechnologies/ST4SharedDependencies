from stobox_dependencies.clients.http import BaseHTTPClient
from stobox_dependencies.schemes.payment_center import UserFeatureConsumeSchema


class PaymentHTTPClient(BaseHTTPClient):
    class ROUTES:
        CHECK_FEATURE: str = '/internal/payments/features/is-enabled'
        CONSUME_USER_FEATURE: str = '/internal/payments/user-feature/consume'

    async def is_feature_enables(self, user_id: int, feature_name: str) -> dict[str, bool]:
        response = await self.get(
            url=self.ROUTES.CHECK_FEATURE,
            params={'user_id': user_id, 'feature_name': feature_name},
        )
        return response.json()

    async def consume_user_feature(self, request_data: UserFeatureConsumeSchema) -> dict[str, bool]:
        response = await self.patch(
            url=self.ROUTES.CONSUME_USER_FEATURE,
            json=request_data,
        )
        return response.json()
