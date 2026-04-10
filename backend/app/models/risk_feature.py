import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class CreateRiskFeatureRequest(BaseModel):
    transaction_id: uuid.UUID
    velocity_1m: int | None = None
    velocity_1h: int | None = None
    amount_zscore: Decimal | None = None
    device_trust_score: Decimal | None = None
    geo_distance_km: Decimal | None = None
    new_beneficiary: bool | None = None
    ip_risk_score: Decimal | None = None
    behavioral_score: Decimal | None = None


class UpdateRiskFeatureRequest(BaseModel):
    velocity_1m: int | None = None
    velocity_1h: int | None = None
    amount_zscore: Decimal | None = None
    device_trust_score: Decimal | None = None
    geo_distance_km: Decimal | None = None
    new_beneficiary: bool | None = None
    ip_risk_score: Decimal | None = None
    behavioral_score: Decimal | None = None


class RiskFeatureResponse(BaseModel):
    id: uuid.UUID
    transaction_id: uuid.UUID
    velocity_1m: int | None
    velocity_1h: int | None
    amount_zscore: Decimal | None
    device_trust_score: Decimal | None
    geo_distance_km: Decimal | None
    new_beneficiary: bool | None
    ip_risk_score: Decimal | None
    behavioral_score: Decimal | None
    created_at: datetime

    model_config = {"from_attributes": True}
