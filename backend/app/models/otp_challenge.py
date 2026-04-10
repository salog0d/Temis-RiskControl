import uuid
from datetime import datetime

from pydantic import BaseModel


class CreateOtpChallengeRequest(BaseModel):
    user_id: uuid.UUID
    transaction_id: uuid.UUID | None = None
    code_hash: str
    channel: str
    status: str = "pending"
    max_attempts: int = 3
    expires_at: datetime


class UpdateOtpChallengeRequest(BaseModel):
    status: str | None = None
    attempts: int | None = None
    verified_at: datetime | None = None


class OtpChallengeResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    transaction_id: uuid.UUID | None
    code_hash: str
    channel: str
    status: str
    attempts: int
    max_attempts: int
    expires_at: datetime
    created_at: datetime
    verified_at: datetime | None

    model_config = {"from_attributes": True}
