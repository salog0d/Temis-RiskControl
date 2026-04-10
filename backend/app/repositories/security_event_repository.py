import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.security_event import SecurityEvent


class SecurityEventRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, user_id: uuid.UUID, type: str, metadata_: dict | None) -> SecurityEvent:
        event = SecurityEvent(user_id=user_id, type=type, metadata_=metadata_)
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def get_by_id(self, event_id: uuid.UUID) -> SecurityEvent | None:
        result = await self.db.execute(select(SecurityEvent).where(SecurityEvent.id == event_id))
        return result.scalar_one_or_none()

    async def get_all(self, user_id: uuid.UUID | None = None) -> list[SecurityEvent]:
        query = select(SecurityEvent)
        if user_id is not None:
            query = query.where(SecurityEvent.user_id == user_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(self, event: SecurityEvent, **fields: object) -> SecurityEvent:
        for key, value in fields.items():
            if value is not None:
                setattr(event, key, value)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def delete(self, event: SecurityEvent) -> None:
        await self.db.delete(event)
        await self.db.commit()
