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


class TokenSchema(BaseModel):
    address: str
    snapshot_id: str
    blockchain_id: str
    project_id: int
    symbol: str
    name: str
    decimals: int
    treasury_address: str
    transaction_hash: str | None
    fireblocks_asset_id: str | None
    is_shadow: bool
    id: int
