import logging

import httpx
from fastapi import APIRouter, HTTPException, status

from app.infra.agent_client import trigger_risk_pipeline
from app.models.webhook import TransactionEventRequest, WebhookResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post(
    "/transaction",
    response_model=WebhookResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Receive a transaction event and trigger the risk control pipeline",
)
async def receive_transaction_event(event: TransactionEventRequest) -> WebhookResponse:
    """
    Event-driven entry point for the risk control pipeline.

    Accepts a structured transaction event payload, validates it, and forwards it
    to the ADK agent service to start the sequential pipeline:
    Risk Engine → Decision Engine → Action Engine.

    The endpoint returns 202 Accepted immediately; the pipeline runs asynchronously
    inside the agent service.
    """
    logger.info(
        "Received transaction event",
        extra={"transaction_id": event.transaction_id, "user_id": event.user_id},
    )

    try:
        await trigger_risk_pipeline(event)
    except httpx.HTTPStatusError as exc:
        logger.error(
            "Agent service returned an error",
            extra={"status_code": exc.response.status_code, "detail": exc.response.text},
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Agent service returned an unexpected error.",
        ) from exc
    except httpx.RequestError as exc:
        logger.error("Could not reach agent service", extra={"error": str(exc)})
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Agent service is unreachable. Please retry later.",
        ) from exc

    return WebhookResponse(
        transaction_id=event.transaction_id,
        status="accepted",
        message="Transaction event accepted and forwarded to the risk control pipeline.",
    )
