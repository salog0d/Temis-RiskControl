import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_usuario(client: AsyncClient) -> None:
    response = await client.post("/api/usuarios", json={"email": "juan@example.com", "telefono": "555-1234"})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "juan@example.com"
    assert data["telefono"] == "555-1234"
    assert data["status"] == "active"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_usuario_duplicate_email(client: AsyncClient) -> None:
    await client.post("/api/usuarios", json={"email": "dup@example.com"})
    response = await client.post("/api/usuarios", json={"email": "dup@example.com"})
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_usuario(client: AsyncClient) -> None:
    create_resp = await client.post("/api/usuarios", json={"email": "get@example.com"})
    user_id = create_resp.json()["id"]

    response = await client.get(f"/api/usuarios/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "get@example.com"


@pytest.mark.asyncio
async def test_get_usuario_not_found(client: AsyncClient) -> None:
    response = await client.get(f"/api/usuarios/{uuid.uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_usuarios(client: AsyncClient) -> None:
    await client.post("/api/usuarios", json={"email": "a@example.com"})
    await client.post("/api/usuarios", json={"email": "b@example.com"})

    response = await client.get("/api/usuarios")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_update_usuario(client: AsyncClient) -> None:
    create_resp = await client.post("/api/usuarios", json={"email": "upd@example.com", "telefono": "111"})
    user_id = create_resp.json()["id"]

    response = await client.patch(f"/api/usuarios/{user_id}", json={"status": "inactive", "telefono": "999"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "inactive"
    assert data["telefono"] == "999"


@pytest.mark.asyncio
async def test_update_usuario_not_found(client: AsyncClient) -> None:
    response = await client.patch(f"/api/usuarios/{uuid.uuid4()}", json={"status": "inactive"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_usuario(client: AsyncClient) -> None:
    create_resp = await client.post("/api/usuarios", json={"email": "del@example.com"})
    user_id = create_resp.json()["id"]

    response = await client.delete(f"/api/usuarios/{user_id}")
    assert response.status_code == 204

    get_resp = await client.get(f"/api/usuarios/{user_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_usuario_not_found(client: AsyncClient) -> None:
    response = await client.delete(f"/api/usuarios/{uuid.uuid4()}")
    assert response.status_code == 404
