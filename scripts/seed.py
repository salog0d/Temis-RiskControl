"""
Seed script — populates the database with 20 dummy users plus related records.

Run from the project root:
    python scripts/seed.py
"""

import asyncio
import random
import uuid
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# ── Entity imports ────────────────────────────────────────────────────────────
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "backend"))

from app.entities.usuario import Usuario
from app.entities.cuenta import Cuenta
from app.entities.dispositivo import Dispositivo
from app.entities.sesion import Sesion
from app.entities.transaccion import Transaccion

import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://temis:temis@localhost:5432/temis_db")

# ── Fake data pools ───────────────────────────────────────────────────────────
NOMBRES = [
    "carlos.mendoza", "sofia.ramirez", "luis.torres", "ana.garcia",
    "jorge.hernandez", "maria.lopez", "pedro.martinez", "laura.sanchez",
    "roberto.diaz", "valentina.morales", "miguel.jimenez", "daniela.reyes",
    "fernando.cruz", "camila.flores", "andres.gomez", "isabella.vargas",
    "pablo.castillo", "natalia.rojas", "diego.medina", "alejandra.ruiz",
]

DOMINIOS = ["gmail.com", "hotmail.com", "yahoo.com.mx", "outlook.com", "protonmail.com"]

CIUDADES_MX = [
    ("Ciudad de México", "MX", 19.4326, -99.1332),
    ("Guadalajara", "MX", 20.6597, -103.3496),
    ("Monterrey", "MX", 25.6866, -100.3161),
    ("Puebla", "MX", 19.0414, -98.2063),
    ("Tijuana", "MX", 32.5027, -117.0039),
    ("Mérida", "MX", 20.9674, -89.5926),
    ("León", "MX", 21.1221, -101.6824),
    ("Querétaro", "MX", 20.5888, -100.3899),
]

DEVICE_TYPES = [
    "iPhone 15 Pro", "Samsung Galaxy S24", "MacBook Pro", "iPad Air",
    "Pixel 8", "Xiaomi 14", "OnePlus 12", "Huawei P60",
]

IPS = [
    "189.203.10.55", "201.145.88.20", "187.190.44.12", "200.33.12.100",
    "148.204.55.10", "177.240.18.90", "189.217.140.32", "201.174.22.8",
]

random.seed(42)


def _rand_date(days_back_min: int, days_back_max: int) -> datetime:
    delta = random.randint(days_back_min, days_back_max)
    return datetime.now(UTC) - timedelta(days=delta)


async def seed(session: AsyncSession) -> None:
    print("Seeding 20 usuarios...")

    for i, nombre in enumerate(NOMBRES):
        dominio = random.choice(DOMINIOS)
        email = f"{nombre}@{dominio}"
        ciudad, pais, lat, lon = random.choice(CIUDADES_MX)
        status = random.choices(["active", "active", "active", "suspended"], weights=[7, 7, 7, 1])[0]

        # ── Usuario ──────────────────────────────────────────────────────────
        usuario = Usuario(
            id=uuid.uuid4(),
            email=email,
            telefono=f"+52 55 {random.randint(1000,9999)} {random.randint(1000,9999)}",
            status=status,
            last_login=_rand_date(0, 30),
            created_at=_rand_date(180, 730),
        )
        session.add(usuario)
        await session.flush()  # ensure usuario.id is persisted before FK references

        # ── Cuenta (1-2 por usuario) ─────────────────────────────────────────
        n_cuentas = random.randint(1, 2)
        cuentas = []
        for _ in range(n_cuentas):
            cuenta = Cuenta(
                id=uuid.uuid4(),
                user_id=usuario.id,
                balance=Decimal(str(round(random.uniform(500, 150_000), 2))),
                currency=random.choice(["MXN", "MXN", "MXN", "USD"]),
                status="active",
            )
            session.add(cuenta)
            cuentas.append(cuenta)

        # ── Dispositivos (1-3 por usuario) ───────────────────────────────────
        n_devices = random.randint(1, 3)
        dispositivos = []
        for j in range(n_devices):
            first_seen = _rand_date(30, 400)
            dispositivo = Dispositivo(
                id=uuid.uuid4(),
                user_id=usuario.id,
                fingerprint=f"{random.choice(DEVICE_TYPES)}-{uuid.uuid4().hex[:8]}",
                trusted=j == 0,  # first device is always trusted
                first_seen=first_seen,
                last_seen=_rand_date(0, 10),
            )
            session.add(dispositivo)
            dispositivos.append(dispositivo)

        # ── Sesiones (2-5 por usuario) ───────────────────────────────────────
        n_sesiones = random.randint(2, 5)
        for _ in range(n_sesiones):
            created = _rand_date(0, 60)
            sesion = Sesion(
                id=uuid.uuid4(),
                user_id=usuario.id,
                device_id=random.choice(dispositivos).id,
                ip=random.choice(IPS),
                country=pais,
                city=ciudad,
                created_at=created,
                ended_at=created + timedelta(minutes=random.randint(5, 120)) if random.random() > 0.2 else None,
            )
            session.add(sesion)

        # ── Transacciones (3-10 por usuario) ─────────────────────────────────
        n_txns = random.randint(3, 10)
        for _ in range(n_txns):
            from_account = random.choice(cuentas) if cuentas else None
            txn = Transaccion(
                id=uuid.uuid4(),
                user_id=usuario.id,
                from_account_id=from_account.id if from_account else None,
                to_account=f"CLABE-{random.randint(10**17, 10**18 - 1)}",
                amount=Decimal(str(round(random.uniform(100, 20_000), 2))),
                currency="MXN",
                status=random.choices(
                    ["completed", "completed", "completed", "pending", "failed"],
                    weights=[6, 6, 6, 1, 1]
                )[0],
                ip=random.choice(IPS),
                device_id=random.choice(dispositivos).id,
                created_at=_rand_date(0, 90),
            )
            session.add(txn)

        print(f"  [{i+1:02d}/20] {email} — {n_cuentas} cuenta(s), {n_devices} dispositivo(s), {n_txns} transaccion(es)")

    await session.commit()
    print("\nSeed completado.")


async def main() -> None:
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        await seed(session)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
