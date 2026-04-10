import uuid
from datetime import datetime

from pydantic import BaseModel


class CreateFraudActionRequest(BaseModel):
    transaction_id: uuid.UUID
    action_type: str
    status: str = "pending"


class UpdateFraudActionRequest(BaseModel):
    action_type: str | None = None
    status: str | None = None


class FraudActionResponse(BaseModel):
    id: uuid.UUID
    transaction_id: uuid.UUID
    action_type: str
    status: str
    executed_at: datetime

    model_config = {"from_attributes": True}
