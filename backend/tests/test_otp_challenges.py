import uuid
from datetime import UTC, datetime, timedelta

import pytest
from httpx import AsyncClient


async def _create_usuario(client: AsyncClient) -> str:
    resp = await client.post("/api/usuarios", json={"email": f"{uuid.uuid4()}@example.com"})
    return resp.json()["id"]


def _future() -> str:
    return (datetime.now(UTC) + timedelta(minutes=10)).isoformat()


@pytest.mark.asyncio
async def test_create_otp_challenge(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    response = await client.post(
        "/api/otp-challenges",
        json={"user_id": user_id, "code_hash": "abc123", "channel": "sms", "expires_at": _future()},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["channel"] == "sms"
    assert data["status"] == "pending"
    assert data["attempts"] == 0
    assert data["max_attempts"] == 3


@pytest.mark.asyncio
async def test_get_otp_challenge(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post(
        "/api/otp-challenges",
        json={"user_id": user_id, "code_hash": "xyz", "channel": "email", "expires_at": _future()},
    )
    challenge_id = create_resp.json()["id"]
    assert (await client.get(f"/api/otp-challenges/{challenge_id}")).status_code == 200


@pytest.mark.asyncio
async def test_get_otp_challenge_not_found(client: AsyncClient) -> None:
    assert (await client.get(f"/api/otp-challenges/{uuid.uuid4()}")).status_code == 404


@pytest.mark.asyncio
async def test_list_otp_challenges_filtered(client: AsyncClient) -> None:
    user_a = await _create_usuario(client)
    user_b = await _create_usuario(client)
    await client.post("/api/otp-challenges", json={"user_id": user_a, "code_hash": "h1", "channel": "sms", "expires_at": _future()})
    await client.post("/api/otp-challenges", json={"user_id": user_b, "code_hash": "h2", "channel": "sms", "expires_at": _future()})
    response = await client.get(f"/api/otp-challenges?user_id={user_a}")
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_update_otp_challenge(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post(
        "/api/otp-challenges",
        json={"user_id": user_id, "code_hash": "h3", "channel": "sms", "expires_at": _future()},
    )
    challenge_id = create_resp.json()["id"]
    response = await client.patch(f"/api/otp-challenges/{challenge_id}", json={"status": "verified", "attempts": 1})
    assert response.status_code == 200
    assert response.json()["status"] == "verified"
    assert response.json()["attempts"] == 1


@pytest.mark.asyncio
async def test_delete_otp_challenge(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post(
        "/api/otp-challenges",
        json={"user_id": user_id, "code_hash": "del", "channel": "sms", "expires_at": _future()},
    )
    challenge_id = create_resp.json()["id"]
    assert (await client.delete(f"/api/otp-challenges/{challenge_id}")).status_code == 204
    assert (await client.get(f"/api/otp-challenges/{challenge_id}")).status_code == 404
