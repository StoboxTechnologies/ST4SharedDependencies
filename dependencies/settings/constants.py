from dependencies import settings

BASE_HTTP_CLIENT_TIMEOUT = 3.0
JWT_ACCESS_TOKEN_ALGORITHMS = ['RS256']
AWS_COGNITO_URL = f'https://cognito-idp.{settings.AWS_DEFAULT_REGION}.amazonaws.com/{settings.COGNITO_POOL_ID}'  # noqa
JWK_URL = '/'.join([AWS_COGNITO_URL.rstrip('/'), '.well-known/jwks.json'])


class ErrorMessages:
    INVALID_ACCESS_TOKEN = 'Invalid access token'  # nosec # noqa S105
    FORBIDDEN_ACCESS_INACTIVE_USER = 'Forbidden access for inactive user'
    FORBIDDEN_ACCESS_KYC_STATE = 'Forbidden access for KYC state'
    FEATURE_NOT_ENABLED = 'Feature {feature} is not enabled for user'

    INVALID_OTP = 'Invalid OTP'
    INVALID_2FA = 'Invalid 2FA'
