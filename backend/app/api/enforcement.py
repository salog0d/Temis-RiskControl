import uuid
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.database.session import get_db
from app.infra.email_client import send_email
from app.repositories.usuario_repository import UsuarioRepository

router = APIRouter(prefix="/enforcement", tags=["enforcement"])


# ── Request models ────────────────────────────────────────────────────────────

class RateLimitRequest(BaseModel):
    user_id: uuid.UUID
    max_transactions: int
    window_minutes: int


class InvalidateSessionsRequest(BaseModel):
    user_id: uuid.UUID


class NotifyEmailRequest(BaseModel):
    user_id: uuid.UUID
    incident_type: str
    decision: str
    reason: str
    challenge_method: str | None = None


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post(
    "/rate-limit",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Apply a temporary transaction rate limit to a user",
)
async def rate_limit_user(
    body: RateLimitRequest,
    db: AsyncSession = Depends(get_db),
) -> None:
    repo = UsuarioRepository(db)
    usuario = await repo.get_by_id(body.user_id)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario not found.")

    until = datetime.now(UTC) + timedelta(minutes=body.window_minutes)
    await repo.update(
        usuario,
        transaction_rate_limited_until=until,
        transaction_rate_limit_max=body.max_transactions,
    )


@router.post(
    "/invalidate-sessions",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Invalidate all active sessions for a user",
)
async def invalidate_sessions(
    body: InvalidateSessionsRequest,
    db: AsyncSession = Depends(get_db),
) -> None:
    repo = UsuarioRepository(db)
    usuario = await repo.get_by_id(body.user_id)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario not found.")

    await repo.update(usuario, sessions_invalidated_at=datetime.now(UTC))


@router.post(
    "/notify-email",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Send a security incident notification email to a user",
)
async def notify_email(
    body: NotifyEmailRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> dict:
    repo = UsuarioRepository(db)
    usuario = await repo.get_by_id(body.user_id)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario not found.")

    background_tasks.add_task(
        send_email,
        recipient=usuario.email,
        incident_type=body.incident_type,
        reason=body.reason,
        challenge_method=body.challenge_method,
    )

    return {"status": "queued", "recipient": usuario.email}
