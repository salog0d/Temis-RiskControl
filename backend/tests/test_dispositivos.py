import uuid

import pytest
from httpx import AsyncClient


async def _create_usuario(client: AsyncClient) -> str:
    resp = await client.post("/api/usuarios", json={"email": f"{uuid.uuid4()}@example.com"})
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_create_dispositivo(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    response = await client.post(
        "/api/dispositivos",
        json={"user_id": user_id, "fingerprint": "abc123", "trusted": False},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user_id
    assert data["fingerprint"] == "abc123"
    assert data["trusted"] is False
    assert "first_seen" in data
    assert "last_seen" in data


@pytest.mark.asyncio
async def test_get_dispositivo(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post(
        "/api/dispositivos",
        json={"user_id": user_id, "fingerprint": "fp-001"},
    )
    dispositivo_id = create_resp.json()["id"]

    response = await client.get(f"/api/dispositivos/{dispositivo_id}")
    assert response.status_code == 200
    assert response.json()["fingerprint"] == "fp-001"


@pytest.mark.asyncio
async def test_get_dispositivo_not_found(client: AsyncClient) -> None:
    response = await client.get(f"/api/dispositivos/{uuid.uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_dispositivos(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    await client.post("/api/dispositivos", json={"user_id": user_id, "fingerprint": "fp-a"})
    await client.post("/api/dispositivos", json={"user_id": user_id, "fingerprint": "fp-b"})

    response = await client.get("/api/dispositivos")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_list_dispositivos_filtered_by_user(client: AsyncClient) -> None:
    user_a = await _create_usuario(client)
    user_b = await _create_usuario(client)
    await client.post("/api/dispositivos", json={"user_id": user_a, "fingerprint": "fp-a"})
    await client.post("/api/dispositivos", json={"user_id": user_b, "fingerprint": "fp-b"})

    response = await client.get(f"/api/dispositivos?user_id={user_a}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == user_a


@pytest.mark.asyncio
async def test_update_dispositivo(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post(
        "/api/dispositivos",
        json={"user_id": user_id, "fingerprint": "fp-old", "trusted": False},
    )
    dispositivo_id = create_resp.json()["id"]

    response = await client.patch(
        f"/api/dispositivos/{dispositivo_id}",
        json={"fingerprint": "fp-new", "trusted": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["fingerprint"] == "fp-new"
    assert data["trusted"] is True


@pytest.mark.asyncio
async def test_update_dispositivo_not_found(client: AsyncClient) -> None:
    response = await client.patch(f"/api/dispositivos/{uuid.uuid4()}", json={"trusted": True})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_touch_dispositivo(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post(
        "/api/dispositivos",
        json={"user_id": user_id, "fingerprint": "fp-touch"},
    )
    dispositivo_id = create_resp.json()["id"]
    original_last_seen = create_resp.json()["last_seen"]

    response = await client.post(f"/api/dispositivos/{dispositivo_id}/touch")
    assert response.status_code == 200
    assert response.json()["last_seen"] >= original_last_seen


@pytest.mark.asyncio
async def test_delete_dispositivo(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post(
        "/api/dispositivos",
        json={"user_id": user_id, "fingerprint": "fp-del"},
    )
    dispositivo_id = create_resp.json()["id"]

    response = await client.delete(f"/api/dispositivos/{dispositivo_id}")
    assert response.status_code == 204

    get_resp = await client.get(f"/api/dispositivos/{dispositivo_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_dispositivo_not_found(client: AsyncClient) -> None:
    response = await client.delete(f"/api/dispositivos/{uuid.uuid4()}")
    assert response.status_code == 404
