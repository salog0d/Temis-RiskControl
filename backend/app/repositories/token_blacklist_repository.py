import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.token_blacklist import TokenBlacklist


class TokenBlacklistRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(
        self, token_jti: str, expires_at: datetime, user_id: uuid.UUID | None, reason: str | None
    ) -> TokenBlacklist:
        entry = TokenBlacklist(user_id=user_id, token_jti=token_jti, expires_at=expires_at, reason=reason)
        self.db.add(entry)
        await self.db.commit()
        await self.db.refresh(entry)
        return entry

    async def get_by_id(self, entry_id: uuid.UUID) -> TokenBlacklist | None:
        result = await self.db.execute(select(TokenBlacklist).where(TokenBlacklist.id == entry_id))
        return result.scalar_one_or_none()

    async def get_by_jti(self, token_jti: str) -> TokenBlacklist | None:
        result = await self.db.execute(select(TokenBlacklist).where(TokenBlacklist.token_jti == token_jti))
        return result.scalar_one_or_none()

    async def get_all(self, user_id: uuid.UUID | None = None) -> list[TokenBlacklist]:
        query = select(TokenBlacklist)
        if user_id is not None:
            query = query.where(TokenBlacklist.user_id == user_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def delete(self, entry: TokenBlacklist) -> None:
        await self.db.delete(entry)
        await self.db.commit()
