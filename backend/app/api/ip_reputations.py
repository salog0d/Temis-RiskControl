import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.ip_reputation import CreateIpReputationRequest, IpReputationResponse, UpdateIpReputationRequest
from app.repositories.ip_reputation_repository import IpReputationRepository

router = APIRouter(prefix="/ip-reputations", tags=["ip-reputations"])


@router.post("", response_model=IpReputationResponse, status_code=status.HTTP_201_CREATED)
async def create_ip_reputation(
    body: CreateIpReputationRequest, db: AsyncSession = Depends(get_db)
) -> IpReputationResponse:
    repo = IpReputationRepository(db)
    try:
        return await repo.create(
            ip=body.ip, status=body.status, failed_attempts=body.failed_attempts, risk_score=body.risk_score
        )
    except IntegrityError:
        raise HTTPException(status_code=409, detail="IP already registered")


@router.get("", response_model=list[IpReputationResponse])
async def list_ip_reputations(db: AsyncSession = Depends(get_db)) -> list[IpReputationResponse]:
    repo = IpReputationRepository(db)
    return await repo.get_all()


@router.get("/by-ip/{ip}", response_model=IpReputationResponse)
async def get_by_ip(ip: str, db: AsyncSession = Depends(get_db)) -> IpReputationResponse:
    repo = IpReputationRepository(db)
    entry = await repo.get_by_ip(ip)
    if not entry:
        raise HTTPException(status_code=404, detail="IP not found")
    return entry


@router.get("/{entry_id}", response_model=IpReputationResponse)
async def get_ip_reputation(entry_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> IpReputationResponse:
    repo = IpReputationRepository(db)
    entry = await repo.get_by_id(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="IP not found")
    return entry


@router.patch("/{entry_id}", response_model=IpReputationResponse)
async def update_ip_reputation(
    entry_id: uuid.UUID, body: UpdateIpReputationRequest, db: AsyncSession = Depends(get_db)
) -> IpReputationResponse:
    repo = IpReputationRepository(db)
    entry = await repo.get_by_id(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="IP not found")
    return await repo.update(
        entry,
        risk_score=body.risk_score,
        status=body.status,
        failed_attempts=body.failed_attempts,
        last_seen=body.last_seen,
    )


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ip_reputation(entry_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    repo = IpReputationRepository(db)
    entry = await repo.get_by_id(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="IP not found")
    await repo.delete(entry)
