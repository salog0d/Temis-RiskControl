import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class CreateRiskAssessmentRequest(BaseModel):
    transaction_id: uuid.UUID
    risk_score: Decimal | None = None
    risk_level: str | None = None
    decision: str | None = None
    reason: dict | None = None


class UpdateRiskAssessmentRequest(BaseModel):
    risk_score: Decimal | None = None
    risk_level: str | None = None
    decision: str | None = None
    reason: dict | None = None


class RiskAssessmentResponse(BaseModel):
    id: uuid.UUID
    transaction_id: uuid.UUID
    risk_score: Decimal | None
    risk_level: str | None
    decision: str | None
    reason: dict | None
    created_at: datetime

    model_config = {"from_attributes": True}
