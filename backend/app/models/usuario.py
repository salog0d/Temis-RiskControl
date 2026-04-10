import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreateUsuarioRequest(BaseModel):
    email: EmailStr
    telefono: str | None = None
    status: str = "active"


class UpdateUsuarioRequest(BaseModel):
    email: EmailStr | None = None
    telefono: str | None = None
    status: str | None = None


class UsuarioResponse(BaseModel):
    id: uuid.UUID
    email: str
    telefono: str | None
    status: str
    last_login: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
