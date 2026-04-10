import uuid
from datetime import datetime

from pydantic import BaseModel


class CreateAuditLogRequest(BaseModel):
    user_id: uuid.UUID | None = None
    transaction_id: uuid.UUID | None = None
    action: str
    resource: str
    details: dict | None = None


class AuditLogResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    transaction_id: uuid.UUID | None
    action: str
    resource: str
    details: dict | None
    created_at: datetime

    model_config = {"from_attributes": True}
