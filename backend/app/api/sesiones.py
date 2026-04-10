import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.sesion import CreateSesionRequest, SesionResponse, UpdateSesionRequest
from app.repositories.sesion_repository import SesionRepository

router = APIRouter(prefix="/sesiones", tags=["sesiones"])


@router.post("", response_model=SesionResponse, status_code=status.HTTP_201_CREATED)
async def create_sesion(body: CreateSesionRequest, db: AsyncSession = Depends(get_db)) -> SesionResponse:
    repo = SesionRepository(db)
    return await repo.create(
        user_id=body.user_id, ip=body.ip, device_id=body.device_id, country=body.country, city=body.city
    )


@router.get("", response_model=list[SesionResponse])
async def list_sesiones(
    user_id: uuid.UUID | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[SesionResponse]:
    repo = SesionRepository(db)
    return await repo.get_all(user_id=user_id)


@router.get("/{sesion_id}", response_model=SesionResponse)
async def get_sesion(sesion_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> SesionResponse:
    repo = SesionRepository(db)
    sesion = await repo.get_by_id(sesion_id)
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesion not found")
    return sesion


@router.patch("/{sesion_id}", response_model=SesionResponse)
async def update_sesion(
    sesion_id: uuid.UUID, body: UpdateSesionRequest, db: AsyncSession = Depends(get_db)
) -> SesionResponse:
    repo = SesionRepository(db)
    sesion = await repo.get_by_id(sesion_id)
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesion not found")
    return await repo.update(sesion, country=body.country, city=body.city, ended_at=body.ended_at)


@router.post("/{sesion_id}/end", response_model=SesionResponse)
async def end_sesion(sesion_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> SesionResponse:
    repo = SesionRepository(db)
    sesion = await repo.get_by_id(sesion_id)
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesion not found")
    return await repo.end(sesion)


@router.delete("/{sesion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sesion(sesion_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    repo = SesionRepository(db)
    sesion = await repo.get_by_id(sesion_id)
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesion not found")
    await repo.delete(sesion)
