import uuid

import pytest
from httpx import AsyncClient


async def _create_usuario(client: AsyncClient) -> str:
    resp = await client.post("/api/usuarios", json={"email": f"{uuid.uuid4()}@example.com"})
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_create_transaccion(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    response = await client.post(
        "/api/transacciones",
        json={"user_id": user_id, "to_account": "EXT-001", "amount": "500.00", "currency": "MXN"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["to_account"] == "EXT-001"
    assert data["status"] == "pending"
    assert data["amount"] == "500.00"


@pytest.mark.asyncio
async def test_get_transaccion(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post(
        "/api/transacciones",
        json={"user_id": user_id, "to_account": "EXT-002", "amount": "100.00", "currency": "USD"},
    )
    tx_id = create_resp.json()["id"]
    response = await client.get(f"/api/transacciones/{tx_id}")
    assert response.status_code == 200
    assert response.json()["currency"] == "USD"


@pytest.mark.asyncio
async def test_get_transaccion_not_found(client: AsyncClient) -> None:
    assert (await client.get(f"/api/transacciones/{uuid.uuid4()}")).status_code == 404


@pytest.mark.asyncio
async def test_list_transacciones_filtered(client: AsyncClient) -> None:
    user_a = await _create_usuario(client)
    user_b = await _create_usuario(client)
    await client.post("/api/transacciones", json={"user_id": user_a, "to_account": "X", "amount": "1.00", "currency": "MXN"})
    await client.post("/api/transacciones", json={"user_id": user_b, "to_account": "Y", "amount": "2.00", "currency": "MXN"})
    response = await client.get(f"/api/transacciones?user_id={user_a}")
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_update_transaccion(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post(
        "/api/transacciones",
        json={"user_id": user_id, "to_account": "EXT-003", "amount": "250.00", "currency": "MXN"},
    )
    tx_id = create_resp.json()["id"]
    response = await client.patch(f"/api/transacciones/{tx_id}", json={"status": "completed"})
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


@pytest.mark.asyncio
async def test_delete_transaccion(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post(
        "/api/transacciones",
        json={"user_id": user_id, "to_account": "EXT-DEL", "amount": "10.00", "currency": "MXN"},
    )
    tx_id = create_resp.json()["id"]
    assert (await client.delete(f"/api/transacciones/{tx_id}")).status_code == 204
    assert (await client.get(f"/api/transacciones/{tx_id}")).status_code == 404


@pytest.mark.asyncio
async def test_delete_transaccion_not_found(client: AsyncClient) -> None:
    assert (await client.delete(f"/api/transacciones/{uuid.uuid4()}")).status_code == 404
