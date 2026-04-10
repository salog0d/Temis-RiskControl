import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.beneficiario import Beneficiario


class BeneficiarioRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, user_id: uuid.UUID, account_number: str, bank_name: str) -> Beneficiario:
        beneficiario = Beneficiario(user_id=user_id, account_number=account_number, bank_name=bank_name)
        self.db.add(beneficiario)
        await self.db.commit()
        await self.db.refresh(beneficiario)
        return beneficiario

    async def get_by_id(self, beneficiario_id: uuid.UUID) -> Beneficiario | None:
        result = await self.db.execute(select(Beneficiario).where(Beneficiario.id == beneficiario_id))
        return result.scalar_one_or_none()

    async def get_all(self, user_id: uuid.UUID | None = None) -> list[Beneficiario]:
        query = select(Beneficiario)
        if user_id is not None:
            query = query.where(Beneficiario.user_id == user_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(self, beneficiario: Beneficiario, **fields: object) -> Beneficiario:
        for key, value in fields.items():
            if value is not None:
                setattr(beneficiario, key, value)
        await self.db.commit()
        await self.db.refresh(beneficiario)
        return beneficiario

    async def delete(self, beneficiario: Beneficiario) -> None:
        await self.db.delete(beneficiario)
        await self.db.commit()
