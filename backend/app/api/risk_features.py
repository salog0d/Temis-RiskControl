import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.risk_feature import CreateRiskFeatureRequest, RiskFeatureResponse, UpdateRiskFeatureRequest
from app.repositories.risk_feature_repository import RiskFeatureRepository

router = APIRouter(prefix="/risk-features", tags=["risk-features"])


@router.post("", response_model=RiskFeatureResponse, status_code=status.HTTP_201_CREATED)
async def create_risk_feature(
    body: CreateRiskFeatureRequest, db: AsyncSession = Depends(get_db)
) -> RiskFeatureResponse:
    repo = RiskFeatureRepository(db)
    return await repo.create(
        transaction_id=body.transaction_id,
        velocity_1m=body.velocity_1m,
        velocity_1h=body.velocity_1h,
        amount_zscore=body.amount_zscore,
        device_trust_score=body.device_trust_score,
        geo_distance_km=body.geo_distance_km,
        new_beneficiary=body.new_beneficiary,
        ip_risk_score=body.ip_risk_score,
        behavioral_score=body.behavioral_score,
    )


@router.get("", response_model=list[RiskFeatureResponse])
async def list_risk_features(
    transaction_id: uuid.UUID | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[RiskFeatureResponse]:
    repo = RiskFeatureRepository(db)
    if transaction_id:
        return await repo.get_by_transaction(transaction_id)
    return await repo.get_all()


@router.get("/{feature_id}", response_model=RiskFeatureResponse)
async def get_risk_feature(feature_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> RiskFeatureResponse:
    repo = RiskFeatureRepository(db)
    feature = await repo.get_by_id(feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail="Risk feature not found")
    return feature


@router.patch("/{feature_id}", response_model=RiskFeatureResponse)
async def update_risk_feature(
    feature_id: uuid.UUID, body: UpdateRiskFeatureRequest, db: AsyncSession = Depends(get_db)
) -> RiskFeatureResponse:
    repo = RiskFeatureRepository(db)
    feature = await repo.get_by_id(feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail="Risk feature not found")
    return await repo.update(
        feature,
        velocity_1m=body.velocity_1m,
        velocity_1h=body.velocity_1h,
        amount_zscore=body.amount_zscore,
        device_trust_score=body.device_trust_score,
        geo_distance_km=body.geo_distance_km,
        new_beneficiary=body.new_beneficiary,
        ip_risk_score=body.ip_risk_score,
        behavioral_score=body.behavioral_score,
    )


@router.delete("/{feature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_risk_feature(feature_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    repo = RiskFeatureRepository(db)
    feature = await repo.get_by_id(feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail="Risk feature not found")
    await repo.delete(feature)
