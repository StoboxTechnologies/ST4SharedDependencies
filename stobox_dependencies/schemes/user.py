from enum import StrEnum

from pydantic import BaseModel


class UserStatus(StrEnum):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'
    SUSPENDED = 'SUSPENDED'


class UserKYCState(StrEnum):
    NOT_STARTED = 'NOT_STARTED'
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'


class User(BaseModel):
    id: int
    is_2fa_enabled: bool
    referral_code: str
    kyc_state: UserKYCState
    status: UserStatus
    has_did: bool | None = None


ACTIVE_USER_STATUSES = (UserStatus.ACTIVE, UserStatus.NEW)
