from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)
app.include_router(api_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Temis RiskControl backend running"}
