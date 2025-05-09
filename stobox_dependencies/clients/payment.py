from pydantic import HttpUrl

from stobox_dependencies.clients.http import BaseHTTPClient
from stobox_dependencies.settings.conf import settings


class PaymentHTTPClient(BaseHTTPClient):
    BASE_URL: HttpUrl = settings.PAYMENT_SERVICE_URL

    class ROUTES:
        CHECK_FEATURE: str = '/internal/payments/features/is-enabled'

    async def is_feature_enables(self, user_id: int, feature_name: str) -> dict[str, bool]:
        response = await self.get(
            url=self.ROUTES.CHECK_FEATURE,
            params={'user_id': user_id, 'feature_name': feature_name},
        )
        return response.json()
