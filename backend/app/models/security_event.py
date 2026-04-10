import uuid
from datetime import datetime

from pydantic import BaseModel


class CreateSecurityEventRequest(BaseModel):
    user_id: uuid.UUID
    type: str
    metadata_: dict | None = None


class UpdateSecurityEventRequest(BaseModel):
    type: str | None = None
    metadata_: dict | None = None


class SecurityEventResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    type: str
    metadata_: dict | None
    created_at: datetime

    model_config = {"from_attributes": True, "populate_by_name": True}
