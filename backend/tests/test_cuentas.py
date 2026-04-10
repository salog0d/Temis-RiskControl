import uuid

import pytest
from httpx import AsyncClient


async def _create_usuario(client: AsyncClient) -> str:
    resp = await client.post("/api/usuarios", json={"email": f"{uuid.uuid4()}@example.com"})
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_create_cuenta(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    response = await client.post(
        "/api/cuentas",
        json={"user_id": user_id, "balance": "1500.00", "currency": "MXN"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user_id
    assert data["balance"] == "1500.00"
    assert data["currency"] == "MXN"
    assert data["status"] == "active"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_cuenta(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post(
        "/api/cuentas",
        json={"user_id": user_id, "balance": "200.00", "currency": "USD"},
    )
    cuenta_id = create_resp.json()["id"]

    response = await client.get(f"/api/cuentas/{cuenta_id}")
    assert response.status_code == 200
    assert response.json()["currency"] == "USD"


@pytest.mark.asyncio
async def test_get_cuenta_not_found(client: AsyncClient) -> None:
    response = await client.get(f"/api/cuentas/{uuid.uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_cuentas(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    await client.post("/api/cuentas", json={"user_id": user_id, "balance": "100.00", "currency": "MXN"})
    await client.post("/api/cuentas", json={"user_id": user_id, "balance": "200.00", "currency": "USD"})

    response = await client.get("/api/cuentas")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_list_cuentas_filtered_by_user(client: AsyncClient) -> None:
    user_a = await _create_usuario(client)
    user_b = await _create_usuario(client)
    await client.post("/api/cuentas", json={"user_id": user_a, "balance": "100.00", "currency": "MXN"})
    await client.post("/api/cuentas", json={"user_id": user_b, "balance": "200.00", "currency": "USD"})

    response = await client.get(f"/api/cuentas?user_id={user_a}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == user_a


@pytest.mark.asyncio
async def test_update_cuenta(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post(
        "/api/cuentas",
        json={"user_id": user_id, "balance": "500.00", "currency": "MXN"},
    )
    cuenta_id = create_resp.json()["id"]

    response = await client.patch(f"/api/cuentas/{cuenta_id}", json={"balance": "999.99", "status": "frozen"})
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == "999.99"
    assert data["status"] == "frozen"


@pytest.mark.asyncio
async def test_update_cuenta_not_found(client: AsyncClient) -> None:
    response = await client.patch(f"/api/cuentas/{uuid.uuid4()}", json={"status": "frozen"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_cuenta(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post(
        "/api/cuentas",
        json={"user_id": user_id, "balance": "0.00", "currency": "MXN"},
    )
    cuenta_id = create_resp.json()["id"]

    response = await client.delete(f"/api/cuentas/{cuenta_id}")
    assert response.status_code == 204

    get_resp = await client.get(f"/api/cuentas/{cuenta_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_cuenta_not_found(client: AsyncClient) -> None:
    response = await client.delete(f"/api/cuentas/{uuid.uuid4()}")
    assert response.status_code == 404
