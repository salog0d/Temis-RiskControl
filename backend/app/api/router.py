from fastapi import APIRouter

from app.api.cuentas import router as cuentas_router
from app.api.dispositivos import router as dispositivos_router
from app.api.health import router as health_router
from app.api.usuarios import router as usuarios_router
from app.api.enforcement import router as enforcement_router
from app.api.webhook import router as webhook_router

api_router = APIRouter(prefix="/api")
api_router.include_router(health_router)
api_router.include_router(usuarios_router)
api_router.include_router(cuentas_router)
api_router.include_router(dispositivos_router)
api_router.include_router(webhook_router)
api_router.include_router(enforcement_router)
