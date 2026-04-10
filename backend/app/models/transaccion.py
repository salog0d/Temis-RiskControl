import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class CreateTransaccionRequest(BaseModel):
    user_id: uuid.UUID
    from_account_id: uuid.UUID | None = None
    to_account: str
    amount: Decimal = Field(gt=0)
    currency: str
    status: str = "pending"
    ip: str | None = None
    device_id: uuid.UUID | None = None


class UpdateTransaccionRequest(BaseModel):
    status: str | None = None
    ip: str | None = None


class TransaccionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    from_account_id: uuid.UUID | None
    to_account: str
    amount: Decimal
    currency: str
    status: str
    ip: str | None
    device_id: uuid.UUID | None
    created_at: datetime

    model_config = {"from_attributes": True}
