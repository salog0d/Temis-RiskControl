import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.cuenta import Cuenta


class CuentaRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, user_id: uuid.UUID, balance: Decimal, currency: str, status: str) -> Cuenta:
        cuenta = Cuenta(user_id=user_id, balance=balance, currency=currency, status=status)
        self.db.add(cuenta)
        await self.db.commit()
        await self.db.refresh(cuenta)
        return cuenta

    async def get_by_id(self, cuenta_id: uuid.UUID) -> Cuenta | None:
        result = await self.db.execute(select(Cuenta).where(Cuenta.id == cuenta_id))
        return result.scalar_one_or_none()

    async def get_all(self, user_id: uuid.UUID | None = None) -> list[Cuenta]:
        query = select(Cuenta)
        if user_id is not None:
            query = query.where(Cuenta.user_id == user_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(self, cuenta: Cuenta, **fields: object) -> Cuenta:
        for key, value in fields.items():
            if value is not None:
                setattr(cuenta, key, value)
        await self.db.commit()
        await self.db.refresh(cuenta)
        return cuenta

    async def delete(self, cuenta: Cuenta) -> None:
        await self.db.delete(cuenta)
        await self.db.commit()
