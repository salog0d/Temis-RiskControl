import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.dispositivo import CreateDispositivoRequest, DispositivoResponse, UpdateDispositivoRequest
from app.repositories.dispositivo_repository import DispositivoRepository

router = APIRouter(prefix="/dispositivos", tags=["dispositivos"])


@router.post("", response_model=DispositivoResponse, status_code=status.HTTP_201_CREATED)
async def create_dispositivo(
    body: CreateDispositivoRequest, db: AsyncSession = Depends(get_db)
) -> DispositivoResponse:
    repo = DispositivoRepository(db)
    return await repo.create(user_id=body.user_id, fingerprint=body.fingerprint, trusted=body.trusted)


@router.get("", response_model=list[DispositivoResponse])
async def list_dispositivos(
    user_id: uuid.UUID | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[DispositivoResponse]:
    repo = DispositivoRepository(db)
    return await repo.get_all(user_id=user_id)


@router.get("/{dispositivo_id}", response_model=DispositivoResponse)
async def get_dispositivo(dispositivo_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> DispositivoResponse:
    repo = DispositivoRepository(db)
    dispositivo = await repo.get_by_id(dispositivo_id)
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo not found")
    return dispositivo


@router.patch("/{dispositivo_id}", response_model=DispositivoResponse)
async def update_dispositivo(
    dispositivo_id: uuid.UUID,
    body: UpdateDispositivoRequest,
    db: AsyncSession = Depends(get_db),
) -> DispositivoResponse:
    repo = DispositivoRepository(db)
    dispositivo = await repo.get_by_id(dispositivo_id)
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo not found")
    return await repo.update(
        dispositivo,
        fingerprint=body.fingerprint,
        trusted=body.trusted,
        last_seen=body.last_seen,
    )


@router.post("/{dispositivo_id}/touch", response_model=DispositivoResponse)
async def touch_dispositivo(dispositivo_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> DispositivoResponse:
    repo = DispositivoRepository(db)
    dispositivo = await repo.get_by_id(dispositivo_id)
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo not found")
    return await repo.touch(dispositivo)


@router.delete("/{dispositivo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dispositivo(dispositivo_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    repo = DispositivoRepository(db)
    dispositivo = await repo.get_by_id(dispositivo_id)
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo not found")
    await repo.delete(dispositivo)
