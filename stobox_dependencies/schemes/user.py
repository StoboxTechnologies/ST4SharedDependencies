from enum import StrEnum

from pydantic import BaseModel


class UserStatus(StrEnum):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'
    SUSPENDED = 'SUSPENDED'
    DISABLED = 'DISABLED'
    OFFLINE = 'OFFLINE'


class UserKYCState(StrEnum):
    NOT_STARTED = 'NOT_STARTED'
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'


class UserFractalState(StrEnum):
    NOT_STARTED = 'NOT_STARTED'
    PENDING = 'PENDING'
    WAITING_SIGNATURE = 'WAITING_SIGNATURE'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    DISABLED = 'DISABLED'


class User(BaseModel):
    id: int
    country_code: str | None
    is_2fa_enabled: bool
    first_name: str | None
    last_name: str | None
    email: str
    referral_code: str
    kyc_state: UserKYCState
    fractal_state: UserFractalState
    status: UserStatus
    has_did: bool | None = None
    stripe_customer_id: str | None = None


ACTIVE_USER_STATUSES = (UserStatus.ACTIVE, UserStatus.NEW)
