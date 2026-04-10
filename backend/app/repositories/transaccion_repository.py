import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.transaccion import Transaccion


class TransaccionRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(
        self,
        user_id: uuid.UUID,
        to_account: str,
        amount: Decimal,
        currency: str,
        status: str,
        from_account_id: uuid.UUID | None,
        ip: str | None,
        device_id: uuid.UUID | None,
    ) -> Transaccion:
        transaccion = Transaccion(
            user_id=user_id,
            from_account_id=from_account_id,
            to_account=to_account,
            amount=amount,
            currency=currency,
            status=status,
            ip=ip,
            device_id=device_id,
        )
        self.db.add(transaccion)
        await self.db.commit()
        await self.db.refresh(transaccion)
        return transaccion

    async def get_by_id(self, transaccion_id: uuid.UUID) -> Transaccion | None:
        result = await self.db.execute(select(Transaccion).where(Transaccion.id == transaccion_id))
        return result.scalar_one_or_none()

    async def get_all(self, user_id: uuid.UUID | None = None) -> list[Transaccion]:
        query = select(Transaccion)
        if user_id is not None:
            query = query.where(Transaccion.user_id == user_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(self, transaccion: Transaccion, **fields: object) -> Transaccion:
        for key, value in fields.items():
            if value is not None:
                setattr(transaccion, key, value)
        await self.db.commit()
        await self.db.refresh(transaccion)
        return transaccion

    async def delete(self, transaccion: Transaccion) -> None:
        await self.db.delete(transaccion)
        await self.db.commit()
