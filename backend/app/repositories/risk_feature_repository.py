import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.risk_feature import RiskFeature


class RiskFeatureRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, transaction_id: uuid.UUID, **fields: object) -> RiskFeature:
        feature = RiskFeature(transaction_id=transaction_id, **fields)
        self.db.add(feature)
        await self.db.commit()
        await self.db.refresh(feature)
        return feature

    async def get_by_id(self, feature_id: uuid.UUID) -> RiskFeature | None:
        result = await self.db.execute(select(RiskFeature).where(RiskFeature.id == feature_id))
        return result.scalar_one_or_none()

    async def get_by_transaction(self, transaction_id: uuid.UUID) -> list[RiskFeature]:
        result = await self.db.execute(select(RiskFeature).where(RiskFeature.transaction_id == transaction_id))
        return list(result.scalars().all())

    async def get_all(self) -> list[RiskFeature]:
        result = await self.db.execute(select(RiskFeature))
        return list(result.scalars().all())

    async def update(self, feature: RiskFeature, **fields: object) -> RiskFeature:
        for key, value in fields.items():
            if value is not None:
                setattr(feature, key, value)
        await self.db.commit()
        await self.db.refresh(feature)
        return feature

    async def delete(self, feature: RiskFeature) -> None:
        await self.db.delete(feature)
        await self.db.commit()
