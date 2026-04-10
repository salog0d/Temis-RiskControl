import uuid
from datetime import datetime

from pydantic import BaseModel


class CreateDispositivoRequest(BaseModel):
    user_id: uuid.UUID
    fingerprint: str
    trusted: bool = False


class UpdateDispositivoRequest(BaseModel):
    fingerprint: str | None = None
    trusted: bool | None = None
    last_seen: datetime | None = None


class DispositivoResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    fingerprint: str
    trusted: bool
    first_seen: datetime
    last_seen: datetime

    model_config = {"from_attributes": True}
