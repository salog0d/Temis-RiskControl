import uuid

import pytest
from httpx import AsyncClient


async def _create_usuario(client: AsyncClient) -> str:
    resp = await client.post("/api/usuarios", json={"email": f"{uuid.uuid4()}@example.com"})
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_create_security_event(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    response = await client.post(
        "/api/security-events",
        json={"user_id": user_id, "type": "login_failed", "metadata_": {"ip": "1.2.3.4"}},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user_id
    assert data["type"] == "login_failed"


@pytest.mark.asyncio
async def test_get_security_event(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post("/api/security-events", json={"user_id": user_id, "type": "suspicious_tx"})
    event_id = create_resp.json()["id"]
    response = await client.get(f"/api/security-events/{event_id}")
    assert response.status_code == 200
    assert response.json()["type"] == "suspicious_tx"


@pytest.mark.asyncio
async def test_get_security_event_not_found(client: AsyncClient) -> None:
    response = await client.get(f"/api/security-events/{uuid.uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_security_events_filtered(client: AsyncClient) -> None:
    user_a = await _create_usuario(client)
    user_b = await _create_usuario(client)
    await client.post("/api/security-events", json={"user_id": user_a, "type": "login"})
    await client.post("/api/security-events", json={"user_id": user_b, "type": "logout"})
    response = await client.get(f"/api/security-events?user_id={user_a}")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_update_security_event(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post("/api/security-events", json={"user_id": user_id, "type": "old_type"})
    event_id = create_resp.json()["id"]
    response = await client.patch(f"/api/security-events/{event_id}", json={"type": "new_type"})
    assert response.status_code == 200
    assert response.json()["type"] == "new_type"


@pytest.mark.asyncio
async def test_delete_security_event(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post("/api/security-events", json={"user_id": user_id, "type": "del"})
    event_id = create_resp.json()["id"]
    assert (await client.delete(f"/api/security-events/{event_id}")).status_code == 204
    assert (await client.get(f"/api/security-events/{event_id}")).status_code == 404


@pytest.mark.asyncio
async def test_delete_security_event_not_found(client: AsyncClient) -> None:
    assert (await client.delete(f"/api/security-events/{uuid.uuid4()}")).status_code == 404
