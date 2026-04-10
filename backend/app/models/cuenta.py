import uuid
from decimal import Decimal

from pydantic import BaseModel, Field


class CreateCuentaRequest(BaseModel):
    user_id: uuid.UUID
    balance: Decimal = Field(default=Decimal("0.00"), ge=0)
    currency: str
    status: str = "active"


class UpdateCuentaRequest(BaseModel):
    balance: Decimal | None = Field(default=None, ge=0)
    currency: str | None = None
    status: str | None = None


class CuentaResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    balance: Decimal
    currency: str
    status: str

    model_config = {"from_attributes": True}
