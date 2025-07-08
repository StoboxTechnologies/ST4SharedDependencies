from stobox_dependencies.clients.http import BaseHTTPClient


class PaymentHTTPClient(BaseHTTPClient):
    class ROUTES:
        CHECK_FEATURE: str = '/internal/payments/features/is-enabled'

    async def is_feature_enables(self, user_id: int, feature_name: str) -> dict[str, bool]:
        response = await self.get(
            url=self.ROUTES.CHECK_FEATURE,
            params={'user_id': user_id, 'feature_name': feature_name},
        )
        return response.json()
