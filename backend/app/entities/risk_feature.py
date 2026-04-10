import uuid
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class RiskFeature(Base):
    __tablename__ = "risk_feature"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    transaction_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("transaccion.id", ondelete="CASCADE"), nullable=False)
    velocity_1m: Mapped[int | None] = mapped_column(Integer, nullable=True)
    velocity_1h: Mapped[int | None] = mapped_column(Integer, nullable=True)
    amount_zscore: Mapped[Decimal | None] = mapped_column(Numeric(precision=10, scale=4), nullable=True)
    device_trust_score: Mapped[Decimal | None] = mapped_column(Numeric(precision=10, scale=4), nullable=True)
    geo_distance_km: Mapped[Decimal | None] = mapped_column(Numeric(precision=10, scale=2), nullable=True)
    new_beneficiary: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    ip_risk_score: Mapped[Decimal | None] = mapped_column(Numeric(precision=10, scale=4), nullable=True)
    behavioral_score: Mapped[Decimal | None] = mapped_column(Numeric(precision=10, scale=4), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
