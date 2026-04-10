import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.risk_assessment import CreateRiskAssessmentRequest, RiskAssessmentResponse, UpdateRiskAssessmentRequest
from app.repositories.risk_assessment_repository import RiskAssessmentRepository

router = APIRouter(prefix="/risk-assessments", tags=["risk-assessments"])


@router.post("", response_model=RiskAssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_risk_assessment(
    body: CreateRiskAssessmentRequest, db: AsyncSession = Depends(get_db)
) -> RiskAssessmentResponse:
    repo = RiskAssessmentRepository(db)
    return await repo.create(
        transaction_id=body.transaction_id,
        risk_score=body.risk_score,
        risk_level=body.risk_level,
        decision=body.decision,
        reason=body.reason,
    )


@router.get("", response_model=list[RiskAssessmentResponse])
async def list_risk_assessments(
    transaction_id: uuid.UUID | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[RiskAssessmentResponse]:
    repo = RiskAssessmentRepository(db)
    if transaction_id:
        return await repo.get_by_transaction(transaction_id)
    return await repo.get_all()


@router.get("/{assessment_id}", response_model=RiskAssessmentResponse)
async def get_risk_assessment(
    assessment_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> RiskAssessmentResponse:
    repo = RiskAssessmentRepository(db)
    assessment = await repo.get_by_id(assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Risk assessment not found")
    return assessment


@router.patch("/{assessment_id}", response_model=RiskAssessmentResponse)
async def update_risk_assessment(
    assessment_id: uuid.UUID, body: UpdateRiskAssessmentRequest, db: AsyncSession = Depends(get_db)
) -> RiskAssessmentResponse:
    repo = RiskAssessmentRepository(db)
    assessment = await repo.get_by_id(assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Risk assessment not found")
    return await repo.update(
        assessment,
        risk_score=body.risk_score,
        risk_level=body.risk_level,
        decision=body.decision,
        reason=body.reason,
    )


@router.delete("/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_risk_assessment(assessment_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    repo = RiskAssessmentRepository(db)
    assessment = await repo.get_by_id(assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Risk assessment not found")
    await repo.delete(assessment)
