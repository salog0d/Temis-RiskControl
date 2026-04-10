import uuid
from datetime import datetime

from pydantic import BaseModel


class CreateSesionRequest(BaseModel):
    user_id: uuid.UUID
    device_id: uuid.UUID | None = None
    ip: str
    country: str | None = None
    city: str | None = None


class UpdateSesionRequest(BaseModel):
    country: str | None = None
    city: str | None = None
    ended_at: datetime | None = None


class SesionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    device_id: uuid.UUID | None
    ip: str
    country: str | None
    city: str | None
    created_at: datetime
    ended_at: datetime | None

    model_config = {"from_attributes": True}
