from enum import StrEnum

from pydantic import BaseModel


class KYBState(StrEnum):
    NOT_STARTED = 'NOT_STARTED'
    PENDING = 'PENDING'
    ON_HOLD = 'ON_HOLD'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'


class Company(BaseModel):
    id: int
    ref: str
    name: str | None
    country: str | None
    kyb_state: KYBState
    has_did: bool
    industry: str | None
    phone_number: str | None
    web_site: str | None
    user_id: int
