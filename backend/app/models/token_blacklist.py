import uuid
from datetime import datetime

from pydantic import BaseModel


class CreateTokenBlacklistRequest(BaseModel):
    user_id: uuid.UUID | None = None
    token_jti: str
    expires_at: datetime
    reason: str | None = None


class TokenBlacklistResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    token_jti: str
    expires_at: datetime
    reason: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
