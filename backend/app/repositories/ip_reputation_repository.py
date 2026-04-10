import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.ip_reputation import IpReputation


class IpReputationRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, ip: str, status: str, failed_attempts: int, risk_score: object) -> IpReputation:
        entry = IpReputation(ip=ip, status=status, failed_attempts=failed_attempts, risk_score=risk_score)
        self.db.add(entry)
        await self.db.commit()
        await self.db.refresh(entry)
        return entry

    async def get_by_id(self, entry_id: uuid.UUID) -> IpReputation | None:
        result = await self.db.execute(select(IpReputation).where(IpReputation.id == entry_id))
        return result.scalar_one_or_none()

    async def get_by_ip(self, ip: str) -> IpReputation | None:
        result = await self.db.execute(select(IpReputation).where(IpReputation.ip == ip))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[IpReputation]:
        result = await self.db.execute(select(IpReputation))
        return list(result.scalars().all())

    async def update(self, entry: IpReputation, **fields: object) -> IpReputation:
        for key, value in fields.items():
            if value is not None:
                setattr(entry, key, value)
        entry.updated_at = datetime.now(UTC)
        await self.db.commit()
        await self.db.refresh(entry)
        return entry

    async def delete(self, entry: IpReputation) -> None:
        await self.db.delete(entry)
        await self.db.commit()
