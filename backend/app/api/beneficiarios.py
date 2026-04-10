import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.beneficiario import BeneficiarioResponse, CreateBeneficiarioRequest, UpdateBeneficiarioRequest
from app.repositories.beneficiario_repository import BeneficiarioRepository

router = APIRouter(prefix="/beneficiarios", tags=["beneficiarios"])


@router.post("", response_model=BeneficiarioResponse, status_code=status.HTTP_201_CREATED)
async def create_beneficiario(
    body: CreateBeneficiarioRequest, db: AsyncSession = Depends(get_db)
) -> BeneficiarioResponse:
    repo = BeneficiarioRepository(db)
    return await repo.create(user_id=body.user_id, account_number=body.account_number, bank_name=body.bank_name)


@router.get("", response_model=list[BeneficiarioResponse])
async def list_beneficiarios(
    user_id: uuid.UUID | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[BeneficiarioResponse]:
    repo = BeneficiarioRepository(db)
    return await repo.get_all(user_id=user_id)


@router.get("/{beneficiario_id}", response_model=BeneficiarioResponse)
async def get_beneficiario(beneficiario_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> BeneficiarioResponse:
    repo = BeneficiarioRepository(db)
    beneficiario = await repo.get_by_id(beneficiario_id)
    if not beneficiario:
        raise HTTPException(status_code=404, detail="Beneficiario not found")
    return beneficiario


@router.patch("/{beneficiario_id}", response_model=BeneficiarioResponse)
async def update_beneficiario(
    beneficiario_id: uuid.UUID,
    body: UpdateBeneficiarioRequest,
    db: AsyncSession = Depends(get_db),
) -> BeneficiarioResponse:
    repo = BeneficiarioRepository(db)
    beneficiario = await repo.get_by_id(beneficiario_id)
    if not beneficiario:
        raise HTTPException(status_code=404, detail="Beneficiario not found")
    return await repo.update(beneficiario, account_number=body.account_number, bank_name=body.bank_name)


@router.delete("/{beneficiario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_beneficiario(beneficiario_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    repo = BeneficiarioRepository(db)
    beneficiario = await repo.get_by_id(beneficiario_id)
    if not beneficiario:
        raise HTTPException(status_code=404, detail="Beneficiario not found")
    await repo.delete(beneficiario)
