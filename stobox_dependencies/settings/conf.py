from enum import Enum

from pydantic import AnyHttpUrl
from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Env(str, Enum):
    TESTING = 'TESTING'
    LOCAL = 'LOCAL'
    DEV = 'DEV'
    DEV_1 = 'DEV_1'
    DEV_2 = 'DEV_2'
    STAGING = 'STAGING'
    PRODUCTION = 'PRODUCTION'


class LogLevel(str, Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class Settings(BaseSettings):
    PORT: int = 4000
    ENV: Env = Env.PRODUCTION
    DEBUG: bool = False
    LOG_LEVEL: str = LogLevel.INFO
    ALLOWED_ORIGINS: str = 'http://localhost http://localhost:3000 http://127.0.0.1:3000'

    SENTRY_DSN: AnyHttpUrl | None = None

    AWS_DEFAULT_REGION: str = 'ue-west-1'
    COGNITO_POOL_ID: str = 'eu-west-1_123456789'
    AWS_ACCESS_KEY_ID: str = ''
    AWS_SECRET_ACCESS_KEY: str = ''
    ALLOWED_ORIGINS_TABLE_NAME: str = 'allowed_origins'

    PAYMENT_SERVICE_URL: HttpUrl = HttpUrl('http://localhost:5000')
    USER_MANAGER_URL: HttpUrl = HttpUrl('http://localhost:5001')
    COMPANY_MANAGER_URL: HttpUrl = HttpUrl('http://localhost:5002')
    PUBLIC_PAGE_URL: HttpUrl = HttpUrl('http://localhost:5003')


settings = Settings()
