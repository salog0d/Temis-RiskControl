import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.usuario import CreateUsuarioRequest, UpdateUsuarioRequest, UsuarioResponse
from app.repositories.usuario_repository import UsuarioRepository

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def create_usuario(body: CreateUsuarioRequest, db: AsyncSession = Depends(get_db)) -> UsuarioResponse:
    repo = UsuarioRepository(db)
    try:
        return await repo.create(email=body.email, telefono=body.telefono, status=body.status)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email already registered")


@router.get("", response_model=list[UsuarioResponse])
async def list_usuarios(db: AsyncSession = Depends(get_db)) -> list[UsuarioResponse]:
    repo = UsuarioRepository(db)
    return await repo.get_all()


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def get_usuario(usuario_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> UsuarioResponse:
    repo = UsuarioRepository(db)
    usuario = await repo.get_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return usuario


@router.patch("/{usuario_id}", response_model=UsuarioResponse)
async def update_usuario(
    usuario_id: uuid.UUID,
    body: UpdateUsuarioRequest,
    db: AsyncSession = Depends(get_db),
) -> UsuarioResponse:
    repo = UsuarioRepository(db)
    usuario = await repo.get_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return await repo.update(usuario, email=body.email, telefono=body.telefono, status=body.status)


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    repo = UsuarioRepository(db)
    usuario = await repo.get_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")
    await repo.delete(usuario)
