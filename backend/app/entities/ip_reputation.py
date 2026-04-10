import uuid
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class IpReputation(Base):
    __tablename__ = "ip_reputation"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    ip: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    risk_score: Mapped[Decimal | None] = mapped_column(Numeric(precision=10, scale=4), nullable=True)
    status: Mapped[str] = mapped_column(String, default="unknown")
    failed_attempts: Mapped[int] = mapped_column(Integer, default=0)
    last_seen: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
