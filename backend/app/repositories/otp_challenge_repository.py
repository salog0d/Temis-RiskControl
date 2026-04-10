import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.otp_challenge import OtpChallenge


class OtpChallengeRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(
        self,
        user_id: uuid.UUID,
        code_hash: str,
        channel: str,
        expires_at: datetime,
        transaction_id: uuid.UUID | None,
        status: str,
        max_attempts: int,
    ) -> OtpChallenge:
        challenge = OtpChallenge(
            user_id=user_id,
            transaction_id=transaction_id,
            code_hash=code_hash,
            channel=channel,
            status=status,
            max_attempts=max_attempts,
            expires_at=expires_at,
        )
        self.db.add(challenge)
        await self.db.commit()
        await self.db.refresh(challenge)
        return challenge

    async def get_by_id(self, challenge_id: uuid.UUID) -> OtpChallenge | None:
        result = await self.db.execute(select(OtpChallenge).where(OtpChallenge.id == challenge_id))
        return result.scalar_one_or_none()

    async def get_all(self, user_id: uuid.UUID | None = None) -> list[OtpChallenge]:
        query = select(OtpChallenge)
        if user_id is not None:
            query = query.where(OtpChallenge.user_id == user_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(self, challenge: OtpChallenge, **fields: object) -> OtpChallenge:
        for key, value in fields.items():
            if value is not None:
                setattr(challenge, key, value)
        await self.db.commit()
        await self.db.refresh(challenge)
        return challenge

    async def delete(self, challenge: OtpChallenge) -> None:
        await self.db.delete(challenge)
        await self.db.commit()
