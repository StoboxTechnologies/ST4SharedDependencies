import logging
from http import HTTPStatus
from typing import Any

import jwt
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from sentry_sdk import set_tag

from stobox_dependencies.settings.constants import AWS_COGNITO_URL
from stobox_dependencies.settings.constants import JWK_URL
from stobox_dependencies.settings.constants import JWT_ACCESS_TOKEN_ALGORITHMS
from stobox_dependencies.settings.constants import ErrorMessages

logger = logging.getLogger(__name__)

oauth2_scheme = HTTPBearer(auto_error=False)
jwk_client = jwt.PyJWKClient(JWK_URL, cache_keys=True)


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail=ErrorMessages.INVALID_ACCESS_TOKEN,
        headers={'WWW-Authenticate': 'Bearer'},
    )


def get_access_token(authorization: HTTPAuthorizationCredentials | None = Depends(oauth2_scheme)) -> str:
    if not authorization:
        raise _unauthorized()
    return authorization.credentials


def get_jwk_key(token: str = Depends(get_access_token)) -> jwt.PyJWK:
    try:
        return jwk_client.get_signing_key_from_jwt(token)
    except jwt.PyJWTError:
        raise _unauthorized()


def validate_access_token(
    token: str = Depends(get_access_token),
    jwk_key: jwt.PyJWK = Depends(get_jwk_key),
) -> dict[str, Any]:
    unauthorized_exc = _unauthorized()

    try:
        token_data = jwt.decode(
            token,
            jwk_key.key,
            algorithms=JWT_ACCESS_TOKEN_ALGORITHMS,
            options={'verify_signature': True, 'verify_exp': True, 'require': ['sub', 'exp', 'iss', 'token_use']},
        )
        if token_data.get('iss') != AWS_COGNITO_URL:
            logger.warning('Invalid "iss" claim')
            raise unauthorized_exc
        if token_data.get('token_use') != 'access':
            logger.warning('Invalid "token_use" claim')
            raise unauthorized_exc

    except jwt.InvalidTokenError as err:
        logger.warning(err)
        raise unauthorized_exc

    else:
        return token_data


async def current_user_id(
    token_payload: dict[str, Any] = Depends(validate_access_token),
) -> int:
    user_id = token_payload['user_id']
    set_tag('user_id', user_id)
    return user_id
