import uuid
from datetime import datetime

from pydantic import BaseModel


class CreateBeneficiarioRequest(BaseModel):
    user_id: uuid.UUID
    account_number: str
    bank_name: str


class UpdateBeneficiarioRequest(BaseModel):
    account_number: str | None = None
    bank_name: str | None = None


class BeneficiarioResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    account_number: str
    bank_name: str
    created_at: datetime

    model_config = {"from_attributes": True}
