import json
import uuid

import httpx

from app.core.config import settings
from app.models.webhook import TransactionEventRequest

_APP_NAME = "risk_control_pipeline"


async def trigger_risk_pipeline(event: TransactionEventRequest) -> dict:
    """
    Sends a transaction event to the ADK agent service to trigger the risk control pipeline.

    Creates a one-off session, then calls POST /run with the event payload as the
    initial user message.  The ADK api_server uses camelCase field names.

    Returns the raw JSON response from the ADK runner, or raises httpx.HTTPError on failure.
    """
    session_id = f"txn-{event.transaction_id}-{uuid.uuid4().hex[:8]}"
    base = settings.agent_service_url

    async with httpx.AsyncClient(timeout=60.0) as client:
        # 1. Create a fresh session for this transaction
        session_resp = await client.post(
            f"{base}/apps/{_APP_NAME}/users/{event.user_id}/sessions",
            json={"id": session_id},
        )
        session_resp.raise_for_status()
        created_session_id = session_resp.json()["id"]

        # 2. Run the pipeline
        run_resp = await client.post(
            f"{base}/run",
            json={
                "appName": _APP_NAME,
                "userId": event.user_id,
                "sessionId": created_session_id,
                "newMessage": {
                    "role": "user",
                    "parts": [{"text": json.dumps(event.model_dump(), ensure_ascii=False)}],
                },
            },
        )
        run_resp.raise_for_status()
        return run_resp.json()
