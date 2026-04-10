import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.security_event import CreateSecurityEventRequest, SecurityEventResponse, UpdateSecurityEventRequest
from app.repositories.security_event_repository import SecurityEventRepository

router = APIRouter(prefix="/security-events", tags=["security-events"])


@router.post("", response_model=SecurityEventResponse, status_code=status.HTTP_201_CREATED)
async def create_security_event(
    body: CreateSecurityEventRequest, db: AsyncSession = Depends(get_db)
) -> SecurityEventResponse:
    repo = SecurityEventRepository(db)
    return await repo.create(user_id=body.user_id, type=body.type, metadata_=body.metadata_)


@router.get("", response_model=list[SecurityEventResponse])
async def list_security_events(
    user_id: uuid.UUID | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[SecurityEventResponse]:
    repo = SecurityEventRepository(db)
    return await repo.get_all(user_id=user_id)


@router.get("/{event_id}", response_model=SecurityEventResponse)
async def get_security_event(event_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> SecurityEventResponse:
    repo = SecurityEventRepository(db)
    event = await repo.get_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Security event not found")
    return event


@router.patch("/{event_id}", response_model=SecurityEventResponse)
async def update_security_event(
    event_id: uuid.UUID, body: UpdateSecurityEventRequest, db: AsyncSession = Depends(get_db)
) -> SecurityEventResponse:
    repo = SecurityEventRepository(db)
    event = await repo.get_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Security event not found")
    return await repo.update(event, type=body.type, metadata_=body.metadata_)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_security_event(event_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    repo = SecurityEventRepository(db)
    event = await repo.get_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Security event not found")
    await repo.delete(event)
