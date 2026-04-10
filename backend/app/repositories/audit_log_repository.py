import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.audit_log import AuditLog


class AuditLogRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(
        self,
        action: str,
        resource: str,
        user_id: uuid.UUID | None,
        transaction_id: uuid.UUID | None,
        details: dict | None,
    ) -> AuditLog:
        log = AuditLog(
            user_id=user_id, transaction_id=transaction_id, action=action, resource=resource, details=details
        )
        self.db.add(log)
        await self.db.commit()
        await self.db.refresh(log)
        return log

    async def get_by_id(self, log_id: uuid.UUID) -> AuditLog | None:
        result = await self.db.execute(select(AuditLog).where(AuditLog.id == log_id))
        return result.scalar_one_or_none()

    async def get_all(self, user_id: uuid.UUID | None = None) -> list[AuditLog]:
        query = select(AuditLog)
        if user_id is not None:
            query = query.where(AuditLog.user_id == user_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def delete(self, log: AuditLog) -> None:
        await self.db.delete(log)
        await self.db.commit()
