import uuid

import pytest
from httpx import AsyncClient


async def _create_usuario(client: AsyncClient) -> str:
    resp = await client.post("/api/usuarios", json={"email": f"{uuid.uuid4()}@example.com"})
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_create_sesion(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    response = await client.post(
        "/api/sesiones",
        json={"user_id": user_id, "ip": "192.168.1.1", "country": "MX", "city": "CDMX"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["ip"] == "192.168.1.1"
    assert data["country"] == "MX"
    assert data["ended_at"] is None


@pytest.mark.asyncio
async def test_get_sesion(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post("/api/sesiones", json={"user_id": user_id, "ip": "10.0.0.1"})
    sesion_id = create_resp.json()["id"]
    response = await client.get(f"/api/sesiones/{sesion_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_sesion_not_found(client: AsyncClient) -> None:
    assert (await client.get(f"/api/sesiones/{uuid.uuid4()}")).status_code == 404


@pytest.mark.asyncio
async def test_list_sesiones_filtered(client: AsyncClient) -> None:
    user_a = await _create_usuario(client)
    user_b = await _create_usuario(client)
    await client.post("/api/sesiones", json={"user_id": user_a, "ip": "1.1.1.1"})
    await client.post("/api/sesiones", json={"user_id": user_b, "ip": "2.2.2.2"})
    response = await client.get(f"/api/sesiones?user_id={user_a}")
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_end_sesion(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post("/api/sesiones", json={"user_id": user_id, "ip": "3.3.3.3"})
    sesion_id = create_resp.json()["id"]
    response = await client.post(f"/api/sesiones/{sesion_id}/end")
    assert response.status_code == 200
    assert response.json()["ended_at"] is not None


@pytest.mark.asyncio
async def test_delete_sesion(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post("/api/sesiones", json={"user_id": user_id, "ip": "4.4.4.4"})
    sesion_id = create_resp.json()["id"]
    assert (await client.delete(f"/api/sesiones/{sesion_id}")).status_code == 204
    assert (await client.get(f"/api/sesiones/{sesion_id}")).status_code == 404


@pytest.mark.asyncio
async def test_delete_sesion_not_found(client: AsyncClient) -> None:
    assert (await client.delete(f"/api/sesiones/{uuid.uuid4()}")).status_code == 404
