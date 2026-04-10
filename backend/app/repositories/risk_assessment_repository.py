import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.risk_assessment import RiskAssessment


class RiskAssessmentRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, transaction_id: uuid.UUID, **fields: object) -> RiskAssessment:
        assessment = RiskAssessment(transaction_id=transaction_id, **fields)
        self.db.add(assessment)
        await self.db.commit()
        await self.db.refresh(assessment)
        return assessment

    async def get_by_id(self, assessment_id: uuid.UUID) -> RiskAssessment | None:
        result = await self.db.execute(select(RiskAssessment).where(RiskAssessment.id == assessment_id))
        return result.scalar_one_or_none()

    async def get_by_transaction(self, transaction_id: uuid.UUID) -> list[RiskAssessment]:
        result = await self.db.execute(
            select(RiskAssessment).where(RiskAssessment.transaction_id == transaction_id)
        )
        return list(result.scalars().all())

    async def get_all(self) -> list[RiskAssessment]:
        result = await self.db.execute(select(RiskAssessment))
        return list(result.scalars().all())

    async def update(self, assessment: RiskAssessment, **fields: object) -> RiskAssessment:
        for key, value in fields.items():
            if value is not None:
                setattr(assessment, key, value)
        await self.db.commit()
        await self.db.refresh(assessment)
        return assessment

    async def delete(self, assessment: RiskAssessment) -> None:
        await self.db.delete(assessment)
        await self.db.commit()
