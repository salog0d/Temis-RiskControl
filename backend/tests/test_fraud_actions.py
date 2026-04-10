import uuid

import pytest
from httpx import AsyncClient


async def _create_usuario(client: AsyncClient) -> str:
    resp = await client.post("/api/usuarios", json={"email": f"{uuid.uuid4()}@example.com"})
    return resp.json()["id"]


async def _create_transaccion(client: AsyncClient, user_id: str) -> str:
    resp = await client.post(
        "/api/transacciones",
        json={"user_id": user_id, "to_account": "EXT", "amount": "100.00", "currency": "MXN"},
    )
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_create_fraud_action(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    tx_id = await _create_transaccion(client, user_id)
    response = await client.post(
        "/api/fraud-actions",
        json={"transaction_id": tx_id, "action_type": "block_account", "status": "pending"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["action_type"] == "block_account"
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_get_fraud_action(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    tx_id = await _create_transaccion(client, user_id)
    create_resp = await client.post("/api/fraud-actions", json={"transaction_id": tx_id, "action_type": "flag"})
    action_id = create_resp.json()["id"]
    assert (await client.get(f"/api/fraud-actions/{action_id}")).status_code == 200


@pytest.mark.asyncio
async def test_get_fraud_action_not_found(client: AsyncClient) -> None:
    assert (await client.get(f"/api/fraud-actions/{uuid.uuid4()}")).status_code == 404


@pytest.mark.asyncio
async def test_list_fraud_actions_by_transaction(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    tx_id = await _create_transaccion(client, user_id)
    await client.post("/api/fraud-actions", json={"transaction_id": tx_id, "action_type": "notify"})
    response = await client.get(f"/api/fraud-actions?transaction_id={tx_id}")
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_update_fraud_action(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    tx_id = await _create_transaccion(client, user_id)
    create_resp = await client.post("/api/fraud-actions", json={"transaction_id": tx_id, "action_type": "hold"})
    action_id = create_resp.json()["id"]
    response = await client.patch(f"/api/fraud-actions/{action_id}", json={"status": "executed"})
    assert response.status_code == 200
    assert response.json()["status"] == "executed"


@pytest.mark.asyncio
async def test_delete_fraud_action(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    tx_id = await _create_transaccion(client, user_id)
    create_resp = await client.post("/api/fraud-actions", json={"transaction_id": tx_id, "action_type": "del"})
    action_id = create_resp.json()["id"]
    assert (await client.delete(f"/api/fraud-actions/{action_id}")).status_code == 204
    assert (await client.get(f"/api/fraud-actions/{action_id}")).status_code == 404
