import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.dispositivo import Dispositivo


class DispositivoRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, user_id: uuid.UUID, fingerprint: str, trusted: bool) -> Dispositivo:
        dispositivo = Dispositivo(user_id=user_id, fingerprint=fingerprint, trusted=trusted)
        self.db.add(dispositivo)
        await self.db.commit()
        await self.db.refresh(dispositivo)
        return dispositivo

    async def get_by_id(self, dispositivo_id: uuid.UUID) -> Dispositivo | None:
        result = await self.db.execute(select(Dispositivo).where(Dispositivo.id == dispositivo_id))
        return result.scalar_one_or_none()

    async def get_all(self, user_id: uuid.UUID | None = None) -> list[Dispositivo]:
        query = select(Dispositivo)
        if user_id is not None:
            query = query.where(Dispositivo.user_id == user_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(self, dispositivo: Dispositivo, **fields: object) -> Dispositivo:
        for key, value in fields.items():
            if value is not None:
                setattr(dispositivo, key, value)
        await self.db.commit()
        await self.db.refresh(dispositivo)
        return dispositivo

    async def touch(self, dispositivo: Dispositivo) -> Dispositivo:
        """Update last_seen to now."""
        dispositivo.last_seen = datetime.now(UTC)
        await self.db.commit()
        await self.db.refresh(dispositivo)
        return dispositivo

    async def delete(self, dispositivo: Dispositivo) -> None:
        await self.db.delete(dispositivo)
        await self.db.commit()
