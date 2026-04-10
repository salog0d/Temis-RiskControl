import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.audit_log import AuditLogResponse, CreateAuditLogRequest
from app.repositories.audit_log_repository import AuditLogRepository

router = APIRouter(prefix="/audit-logs", tags=["audit-logs"])


@router.post("", response_model=AuditLogResponse, status_code=status.HTTP_201_CREATED)
async def create_audit_log(body: CreateAuditLogRequest, db: AsyncSession = Depends(get_db)) -> AuditLogResponse:
    repo = AuditLogRepository(db)
    return await repo.create(
        action=body.action,
        resource=body.resource,
        user_id=body.user_id,
        transaction_id=body.transaction_id,
        details=body.details,
    )


@router.get("", response_model=list[AuditLogResponse])
async def list_audit_logs(
    user_id: uuid.UUID | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[AuditLogResponse]:
    repo = AuditLogRepository(db)
    return await repo.get_all(user_id=user_id)


@router.get("/{log_id}", response_model=AuditLogResponse)
async def get_audit_log(log_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> AuditLogResponse:
    repo = AuditLogRepository(db)
    log = await repo.get_by_id(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return log


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_audit_log(log_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    repo = AuditLogRepository(db)
    log = await repo.get_by_id(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    await repo.delete(log)
