import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.token_blacklist import CreateTokenBlacklistRequest, TokenBlacklistResponse
from app.repositories.token_blacklist_repository import TokenBlacklistRepository

router = APIRouter(prefix="/token-blacklist", tags=["token-blacklist"])


@router.post("", response_model=TokenBlacklistResponse, status_code=status.HTTP_201_CREATED)
async def create_token_blacklist(
    body: CreateTokenBlacklistRequest, db: AsyncSession = Depends(get_db)
) -> TokenBlacklistResponse:
    repo = TokenBlacklistRepository(db)
    return await repo.create(
        token_jti=body.token_jti, expires_at=body.expires_at, user_id=body.user_id, reason=body.reason
    )


@router.get("", response_model=list[TokenBlacklistResponse])
async def list_token_blacklist(
    user_id: uuid.UUID | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[TokenBlacklistResponse]:
    repo = TokenBlacklistRepository(db)
    return await repo.get_all(user_id=user_id)


@router.get("/by-jti/{token_jti}", response_model=TokenBlacklistResponse)
async def get_by_jti(token_jti: str, db: AsyncSession = Depends(get_db)) -> TokenBlacklistResponse:
    repo = TokenBlacklistRepository(db)
    entry = await repo.get_by_jti(token_jti)
    if not entry:
        raise HTTPException(status_code=404, detail="Token not found in blacklist")
    return entry


@router.get("/{entry_id}", response_model=TokenBlacklistResponse)
async def get_token_blacklist(entry_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> TokenBlacklistResponse:
    repo = TokenBlacklistRepository(db)
    entry = await repo.get_by_id(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Token not found in blacklist")
    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_token_blacklist(entry_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    repo = TokenBlacklistRepository(db)
    entry = await repo.get_by_id(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Token not found in blacklist")
    await repo.delete(entry)
