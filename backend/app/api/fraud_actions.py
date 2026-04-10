import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.fraud_action import CreateFraudActionRequest, FraudActionResponse, UpdateFraudActionRequest
from app.repositories.fraud_action_repository import FraudActionRepository

router = APIRouter(prefix="/fraud-actions", tags=["fraud-actions"])


@router.post("", response_model=FraudActionResponse, status_code=status.HTTP_201_CREATED)
async def create_fraud_action(
    body: CreateFraudActionRequest, db: AsyncSession = Depends(get_db)
) -> FraudActionResponse:
    repo = FraudActionRepository(db)
    return await repo.create(
        transaction_id=body.transaction_id, action_type=body.action_type, status=body.status
    )


@router.get("", response_model=list[FraudActionResponse])
async def list_fraud_actions(
    transaction_id: uuid.UUID | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[FraudActionResponse]:
    repo = FraudActionRepository(db)
    if transaction_id:
        return await repo.get_by_transaction(transaction_id)
    return await repo.get_all()


@router.get("/{action_id}", response_model=FraudActionResponse)
async def get_fraud_action(action_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> FraudActionResponse:
    repo = FraudActionRepository(db)
    action = await repo.get_by_id(action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Fraud action not found")
    return action


@router.patch("/{action_id}", response_model=FraudActionResponse)
async def update_fraud_action(
    action_id: uuid.UUID, body: UpdateFraudActionRequest, db: AsyncSession = Depends(get_db)
) -> FraudActionResponse:
    repo = FraudActionRepository(db)
    action = await repo.get_by_id(action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Fraud action not found")
    return await repo.update(action, action_type=body.action_type, status=body.status)


@router.delete("/{action_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fraud_action(action_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    repo = FraudActionRepository(db)
    action = await repo.get_by_id(action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Fraud action not found")
    await repo.delete(action)
