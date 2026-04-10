import json
import uuid

import httpx

from app.core.config import settings
from app.models.webhook import TransactionEventRequest


async def trigger_risk_pipeline(event: TransactionEventRequest) -> dict:
    """
    Sends a transaction event to the ADK agent service to trigger the risk control pipeline.

    The ADK web server exposes POST /run which accepts a user message. The event payload
    is serialised as JSON and forwarded as the initial user message.

    Returns the raw JSON response from the ADK runner, or raises httpx.HTTPError on failure.
    """
    session_id = f"txn-{event.transaction_id}-{uuid.uuid4().hex[:8]}"

    body = {
        "app_name": "risk_control_pipeline",
        "user_id": event.user_id,
        "session_id": session_id,
        "new_message": {
            "role": "user",
            "parts": [{"text": json.dumps(event.model_dump(), ensure_ascii=False)}],
        },
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{settings.agent_service_url}/run",
            json=body,
        )
        response.raise_for_status()
        return response.json()
