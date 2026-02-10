from stobox_dependencies.clients.http import BaseHTTPClient
from stobox_dependencies.schemes.user import User


class UserHTTPClient(BaseHTTPClient):
    class ROUTES:
        USER_INFO: str = '/internal/users/{user_id}'
        OTP_VERIFY: str = '/users/security/otp/verify'
        TWO_FA_VERIFY: str = '/users/security/2fa/verify'
        OTP_TWO_FA_VERIFY: str = '/internal/users/security/verify/2fa-otp'

    async def get_user_info(self, user_id: int | str) -> User:
        response = await self.get(url=self.ROUTES.USER_INFO.format(user_id=user_id))
        return User.model_validate(response.json())

    async def verify_otp(self, token: str, otp_code: str) -> None:
        await self.post(
            url=self.ROUTES.OTP_VERIFY,
            headers={
                'Authorization': f'Bearer {token}',
                'secret-otp': otp_code,
            },
        )

    async def verify_2fa(self, token: str, two_fa_code: str) -> None:
        await self.post(
            url=self.ROUTES.TWO_FA_VERIFY,
            headers={
                'Authorization': f'Bearer {token}',
                'secret-2fa': two_fa_code,
            },
        )

    async def verify_otp_2fa(self, user_id: int, otp_code: str, two_fa_code: str | None) -> None:
        await self.post(
            url=self.ROUTES.OTP_TWO_FA_VERIFY,
            json={
                'user_id': user_id,
                'secret_2fa': two_fa_code,
                'secret_otp': otp_code,
            },
        )
