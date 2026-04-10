import os

import httpx

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")


def block_account(account_id: str, user_id: str) -> dict:
    """
    Blocks a user's account by setting its status to 'blocked' via the backend API.
    Call this when decision is 'decline' and action_hints.block_transaction is true.

    Args:
        account_id: UUID of the Cuenta to block.
        user_id: UUID of the owning Usuario (used for audit context).

    Returns:
        dict with 'success', 'account_id', and 'detail'.
    """
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.patch(
                f"{BACKEND_URL}/api/cuentas/{account_id}",
                json={"status": "blocked"},
            )
            response.raise_for_status()
        return {
            "success": True,
            "account_id": account_id,
            "detail": f"Account {account_id} blocked for user {user_id}.",
        }
    except httpx.HTTPStatusError as exc:
        return {
            "success": False,
            "account_id": account_id,
            "detail": f"Backend returned {exc.response.status_code}: {exc.response.text}",
        }
    except httpx.RequestError as exc:
        return {
            "success": False,
            "account_id": account_id,
            "detail": f"Backend unreachable: {exc}",
        }


def apply_transaction_rate_limit(
    user_id: str,
    max_transactions: int,
    window_minutes: int,
) -> dict:
    """
    Applies a temporary rate limit on transaction submissions for a user.
    Use for 'review' decisions (max=1, window=60) or elevated 'challenge' decisions
    (max=3, window=30) to slow down potential fraud while the case is evaluated.

    Args:
        user_id: UUID of the Usuario to rate-limit.
        max_transactions: Maximum transactions allowed within the window.
        window_minutes: Duration of the rate-limit window in minutes.

    Returns:
        dict with 'success', 'user_id', and 'detail'.
    """
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{BACKEND_URL}/api/enforcement/rate-limit",
                json={
                    "user_id": user_id,
                    "max_transactions": max_transactions,
                    "window_minutes": window_minutes,
                },
            )
            response.raise_for_status()
        return {
            "success": True,
            "user_id": user_id,
            "detail": (
                f"Rate limit applied: max {max_transactions} transactions "
                f"per {window_minutes} min for user {user_id}."
            ),
        }
    except httpx.HTTPStatusError as exc:
        return {
            "success": False,
            "user_id": user_id,
            "detail": f"Backend returned {exc.response.status_code}: {exc.response.text}",
        }
    except httpx.RequestError as exc:
        return {
            "success": False,
            "user_id": user_id,
            "detail": f"Backend unreachable: {exc}",
        }


def invalidate_user_sessions(user_id: str) -> dict:
    """
    Invalidates all active sessions for a user, forcing re-authentication on the next request.
    Call this when action_hints.freeze_account is true (ATO confirmed or fraud network detected).

    Args:
        user_id: UUID of the Usuario whose sessions should be invalidated.

    Returns:
        dict with 'success', 'user_id', and 'detail'.
    """
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{BACKEND_URL}/api/enforcement/invalidate-sessions",
                json={"user_id": user_id},
            )
            response.raise_for_status()
        return {
            "success": True,
            "user_id": user_id,
            "detail": f"All sessions invalidated for user {user_id}.",
        }
    except httpx.HTTPStatusError as exc:
        return {
            "success": False,
            "user_id": user_id,
            "detail": f"Backend returned {exc.response.status_code}: {exc.response.text}",
        }
    except httpx.RequestError as exc:
        return {
            "success": False,
            "user_id": user_id,
            "detail": f"Backend unreachable: {exc}",
        }


def send_incident_email(
    user_id: str,
    incident_type: str,
    decision: str,
    reason: str,
    challenge_method: str | None = None,
) -> dict:
    """
    Sends a security incident notification email to the user via the backend notification service.
    Call whenever action_hints.notify_user is true.

    incident_type values:
      - 'fraud_alert'         → transaction blocked or flagged for review
      - 'challenge_required'  → step-up authentication needed before proceeding
      - 'account_blocked'     → account suspended due to confirmed compromise
      - 'rate_limited'        → temporary transaction limits applied

    Args:
        user_id: UUID of the Usuario to notify (backend resolves the email address).
        incident_type: One of the values above.
        decision: Pipeline decision ('approve'|'challenge'|'review'|'decline').
        reason: Human-readable reason from the Decision Engine.
        challenge_method: For challenge decisions: 'otp_sms'|'otp_email'|None.

    Returns:
        dict with 'success', 'user_id', and 'detail'.
    """
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{BACKEND_URL}/api/enforcement/notify-email",
                json={
                    "user_id": user_id,
                    "incident_type": incident_type,
                    "decision": decision,
                    "reason": reason,
                    "challenge_method": challenge_method,
                },
            )
            response.raise_for_status()
        return {
            "success": True,
            "user_id": user_id,
            "detail": f"Incident email '{incident_type}' queued for user {user_id}.",
        }
    except httpx.HTTPStatusError as exc:
        return {
            "success": False,
            "user_id": user_id,
            "detail": f"Backend returned {exc.response.status_code}: {exc.response.text}",
        }
    except httpx.RequestError as exc:
        return {
            "success": False,
            "user_id": user_id,
            "detail": f"Backend unreachable: {exc}",
        }
