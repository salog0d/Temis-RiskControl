import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.fraud_action import FraudAction


class FraudActionRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, transaction_id: uuid.UUID, action_type: str, status: str) -> FraudAction:
        action = FraudAction(transaction_id=transaction_id, action_type=action_type, status=status)
        self.db.add(action)
        await self.db.commit()
        await self.db.refresh(action)
        return action

    async def get_by_id(self, action_id: uuid.UUID) -> FraudAction | None:
        result = await self.db.execute(select(FraudAction).where(FraudAction.id == action_id))
        return result.scalar_one_or_none()

    async def get_by_transaction(self, transaction_id: uuid.UUID) -> list[FraudAction]:
        result = await self.db.execute(select(FraudAction).where(FraudAction.transaction_id == transaction_id))
        return list(result.scalars().all())

    async def get_all(self) -> list[FraudAction]:
        result = await self.db.execute(select(FraudAction))
        return list(result.scalars().all())

    async def update(self, action: FraudAction, **fields: object) -> FraudAction:
        for key, value in fields.items():
            if value is not None:
                setattr(action, key, value)
        await self.db.commit()
        await self.db.refresh(action)
        return action

    async def delete(self, action: FraudAction) -> None:
        await self.db.delete(action)
        await self.db.commit()
