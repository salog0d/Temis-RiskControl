from fastapi import APIRouter

from app.api.audit_logs import router as audit_logs_router
from app.api.beneficiarios import router as beneficiarios_router
from app.api.cuentas import router as cuentas_router
from app.api.dispositivos import router as dispositivos_router
from app.api.fraud_actions import router as fraud_actions_router
from app.api.health import router as health_router
from app.api.ip_reputations import router as ip_reputations_router
from app.api.otp_challenges import router as otp_challenges_router
from app.api.risk_assessments import router as risk_assessments_router
from app.api.risk_features import router as risk_features_router
from app.api.security_events import router as security_events_router
from app.api.sesiones import router as sesiones_router
from app.api.token_blacklist import router as token_blacklist_router
from app.api.transacciones import router as transacciones_router
from app.api.usuarios import router as usuarios_router
from app.api.enforcement import router as enforcement_router
from app.api.webhook import router as webhook_router

api_router = APIRouter(prefix="/api")
api_router.include_router(health_router)
api_router.include_router(usuarios_router)
api_router.include_router(cuentas_router)
api_router.include_router(dispositivos_router)
api_router.include_router(beneficiarios_router)
api_router.include_router(sesiones_router)
api_router.include_router(transacciones_router)
api_router.include_router(security_events_router)
api_router.include_router(risk_features_router)
api_router.include_router(risk_assessments_router)
api_router.include_router(fraud_actions_router)
api_router.include_router(audit_logs_router)
api_router.include_router(otp_challenges_router)
api_router.include_router(token_blacklist_router)
api_router.include_router(ip_reputations_router)
api_router.include_router(webhook_router)
api_router.include_router(enforcement_router)
