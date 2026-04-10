import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.usuario import Usuario


class UsuarioRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, email: str, telefono: str | None, status: str) -> Usuario:
        usuario = Usuario(email=email, telefono=telefono, status=status)
        self.db.add(usuario)
        await self.db.commit()
        await self.db.refresh(usuario)
        return usuario

    async def get_by_id(self, usuario_id: uuid.UUID) -> Usuario | None:
        result = await self.db.execute(select(Usuario).where(Usuario.id == usuario_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Usuario]:
        result = await self.db.execute(select(Usuario))
        return list(result.scalars().all())

    async def update(self, usuario: Usuario, **fields: object) -> Usuario:
        for key, value in fields.items():
            if value is not None:
                setattr(usuario, key, value)
        await self.db.commit()
        await self.db.refresh(usuario)
        return usuario

    async def delete(self, usuario: Usuario) -> None:
        await self.db.delete(usuario)
        await self.db.commit()
