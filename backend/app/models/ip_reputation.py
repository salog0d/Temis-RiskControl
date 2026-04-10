import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class CreateIpReputationRequest(BaseModel):
    ip: str
    risk_score: Decimal | None = None
    status: str = "unknown"
    failed_attempts: int = 0


class UpdateIpReputationRequest(BaseModel):
    risk_score: Decimal | None = None
    status: str | None = None
    failed_attempts: int | None = None
    last_seen: datetime | None = None


class IpReputationResponse(BaseModel):
    id: uuid.UUID
    ip: str
    risk_score: Decimal | None
    status: str
    failed_attempts: int
    last_seen: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
