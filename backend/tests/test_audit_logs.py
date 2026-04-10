import uuid

import pytest
from httpx import AsyncClient


async def _create_usuario(client: AsyncClient) -> str:
    resp = await client.post("/api/usuarios", json={"email": f"{uuid.uuid4()}@example.com"})
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_create_audit_log(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    response = await client.post(
        "/api/audit-logs",
        json={"user_id": user_id, "action": "login", "resource": "sesion", "details": {"browser": "Chrome"}},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["action"] == "login"
    assert data["details"]["browser"] == "Chrome"


@pytest.mark.asyncio
async def test_create_audit_log_no_user(client: AsyncClient) -> None:
    response = await client.post("/api/audit-logs", json={"action": "system_boot", "resource": "server"})
    assert response.status_code == 201
    assert response.json()["user_id"] is None


@pytest.mark.asyncio
async def test_get_audit_log(client: AsyncClient) -> None:
    create_resp = await client.post("/api/audit-logs", json={"action": "read", "resource": "cuenta"})
    log_id = create_resp.json()["id"]
    assert (await client.get(f"/api/audit-logs/{log_id}")).status_code == 200


@pytest.mark.asyncio
async def test_get_audit_log_not_found(client: AsyncClient) -> None:
    assert (await client.get(f"/api/audit-logs/{uuid.uuid4()}")).status_code == 404


@pytest.mark.asyncio
async def test_list_audit_logs_filtered(client: AsyncClient) -> None:
    user_a = await _create_usuario(client)
    user_b = await _create_usuario(client)
    await client.post("/api/audit-logs", json={"user_id": user_a, "action": "login", "resource": "sesion"})
    await client.post("/api/audit-logs", json={"user_id": user_b, "action": "login", "resource": "sesion"})
    response = await client.get(f"/api/audit-logs?user_id={user_a}")
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_delete_audit_log(client: AsyncClient) -> None:
    create_resp = await client.post("/api/audit-logs", json={"action": "del", "resource": "X"})
    log_id = create_resp.json()["id"]
    assert (await client.delete(f"/api/audit-logs/{log_id}")).status_code == 204
    assert (await client.get(f"/api/audit-logs/{log_id}")).status_code == 404


@pytest.mark.asyncio
async def test_delete_audit_log_not_found(client: AsyncClient) -> None:
    assert (await client.delete(f"/api/audit-logs/{uuid.uuid4()}")).status_code == 404
