import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.sesion import Sesion


class SesionRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(
        self, user_id: uuid.UUID, ip: str, device_id: uuid.UUID | None, country: str | None, city: str | None
    ) -> Sesion:
        sesion = Sesion(user_id=user_id, ip=ip, device_id=device_id, country=country, city=city)
        self.db.add(sesion)
        await self.db.commit()
        await self.db.refresh(sesion)
        return sesion

    async def get_by_id(self, sesion_id: uuid.UUID) -> Sesion | None:
        result = await self.db.execute(select(Sesion).where(Sesion.id == sesion_id))
        return result.scalar_one_or_none()

    async def get_all(self, user_id: uuid.UUID | None = None) -> list[Sesion]:
        query = select(Sesion)
        if user_id is not None:
            query = query.where(Sesion.user_id == user_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(self, sesion: Sesion, **fields: object) -> Sesion:
        for key, value in fields.items():
            if value is not None:
                setattr(sesion, key, value)
        await self.db.commit()
        await self.db.refresh(sesion)
        return sesion

    async def end(self, sesion: Sesion) -> Sesion:
        sesion.ended_at = datetime.now(UTC)
        await self.db.commit()
        await self.db.refresh(sesion)
        return sesion

    async def delete(self, sesion: Sesion) -> None:
        await self.db.delete(sesion)
        await self.db.commit()
