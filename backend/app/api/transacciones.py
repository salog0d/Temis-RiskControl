import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.transaccion import CreateTransaccionRequest, TransaccionResponse, UpdateTransaccionRequest
from app.repositories.transaccion_repository import TransaccionRepository

router = APIRouter(prefix="/transacciones", tags=["transacciones"])


@router.post("", response_model=TransaccionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaccion(
    body: CreateTransaccionRequest, db: AsyncSession = Depends(get_db)
) -> TransaccionResponse:
    repo = TransaccionRepository(db)
    return await repo.create(
        user_id=body.user_id,
        from_account_id=body.from_account_id,
        to_account=body.to_account,
        amount=body.amount,
        currency=body.currency,
        status=body.status,
        ip=body.ip,
        device_id=body.device_id,
    )


@router.get("", response_model=list[TransaccionResponse])
async def list_transacciones(
    user_id: uuid.UUID | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[TransaccionResponse]:
    repo = TransaccionRepository(db)
    return await repo.get_all(user_id=user_id)


@router.get("/{transaccion_id}", response_model=TransaccionResponse)
async def get_transaccion(transaccion_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> TransaccionResponse:
    repo = TransaccionRepository(db)
    transaccion = await repo.get_by_id(transaccion_id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transaccion not found")
    return transaccion


@router.patch("/{transaccion_id}", response_model=TransaccionResponse)
async def update_transaccion(
    transaccion_id: uuid.UUID, body: UpdateTransaccionRequest, db: AsyncSession = Depends(get_db)
) -> TransaccionResponse:
    repo = TransaccionRepository(db)
    transaccion = await repo.get_by_id(transaccion_id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transaccion not found")
    return await repo.update(transaccion, status=body.status, ip=body.ip)


@router.delete("/{transaccion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaccion(transaccion_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    repo = TransaccionRepository(db)
    transaccion = await repo.get_by_id(transaccion_id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transaccion not found")
    await repo.delete(transaccion)
