import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.cuenta import CreateCuentaRequest, CuentaResponse, UpdateCuentaRequest
from app.repositories.cuenta_repository import CuentaRepository

router = APIRouter(prefix="/cuentas", tags=["cuentas"])


@router.post("", response_model=CuentaResponse, status_code=status.HTTP_201_CREATED)
async def create_cuenta(body: CreateCuentaRequest, db: AsyncSession = Depends(get_db)) -> CuentaResponse:
    repo = CuentaRepository(db)
    return await repo.create(
        user_id=body.user_id,
        balance=body.balance,
        currency=body.currency,
        status=body.status,
    )


@router.get("", response_model=list[CuentaResponse])
async def list_cuentas(
    user_id: uuid.UUID | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[CuentaResponse]:
    repo = CuentaRepository(db)
    return await repo.get_all(user_id=user_id)


@router.get("/{cuenta_id}", response_model=CuentaResponse)
async def get_cuenta(cuenta_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> CuentaResponse:
    repo = CuentaRepository(db)
    cuenta = await repo.get_by_id(cuenta_id)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta not found")
    return cuenta


@router.patch("/{cuenta_id}", response_model=CuentaResponse)
async def update_cuenta(
    cuenta_id: uuid.UUID,
    body: UpdateCuentaRequest,
    db: AsyncSession = Depends(get_db),
) -> CuentaResponse:
    repo = CuentaRepository(db)
    cuenta = await repo.get_by_id(cuenta_id)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta not found")
    return await repo.update(cuenta, balance=body.balance, currency=body.currency, status=body.status)


@router.delete("/{cuenta_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cuenta(cuenta_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    repo = CuentaRepository(db)
    cuenta = await repo.get_by_id(cuenta_id)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta not found")
    await repo.delete(cuenta)
