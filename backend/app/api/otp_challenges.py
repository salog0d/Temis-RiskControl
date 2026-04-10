import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.otp_challenge import CreateOtpChallengeRequest, OtpChallengeResponse, UpdateOtpChallengeRequest
from app.repositories.otp_challenge_repository import OtpChallengeRepository

router = APIRouter(prefix="/otp-challenges", tags=["otp-challenges"])


@router.post("", response_model=OtpChallengeResponse, status_code=status.HTTP_201_CREATED)
async def create_otp_challenge(
    body: CreateOtpChallengeRequest, db: AsyncSession = Depends(get_db)
) -> OtpChallengeResponse:
    repo = OtpChallengeRepository(db)
    return await repo.create(
        user_id=body.user_id,
        transaction_id=body.transaction_id,
        code_hash=body.code_hash,
        channel=body.channel,
        status=body.status,
        max_attempts=body.max_attempts,
        expires_at=body.expires_at,
    )


@router.get("", response_model=list[OtpChallengeResponse])
async def list_otp_challenges(
    user_id: uuid.UUID | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[OtpChallengeResponse]:
    repo = OtpChallengeRepository(db)
    return await repo.get_all(user_id=user_id)


@router.get("/{challenge_id}", response_model=OtpChallengeResponse)
async def get_otp_challenge(challenge_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> OtpChallengeResponse:
    repo = OtpChallengeRepository(db)
    challenge = await repo.get_by_id(challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="OTP challenge not found")
    return challenge


@router.patch("/{challenge_id}", response_model=OtpChallengeResponse)
async def update_otp_challenge(
    challenge_id: uuid.UUID, body: UpdateOtpChallengeRequest, db: AsyncSession = Depends(get_db)
) -> OtpChallengeResponse:
    repo = OtpChallengeRepository(db)
    challenge = await repo.get_by_id(challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="OTP challenge not found")
    return await repo.update(challenge, status=body.status, attempts=body.attempts, verified_at=body.verified_at)


@router.delete("/{challenge_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_otp_challenge(challenge_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    repo = OtpChallengeRepository(db)
    challenge = await repo.get_by_id(challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="OTP challenge not found")
    await repo.delete(challenge)
