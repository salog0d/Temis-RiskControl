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
async def test_create_risk_feature(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    tx_id = await _create_transaccion(client, user_id)
    response = await client.post(
        "/api/risk-features",
        json={"transaction_id": tx_id, "velocity_1m": 3, "velocity_1h": 10, "new_beneficiary": True},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["velocity_1m"] == 3
    assert data["new_beneficiary"] is True


@pytest.mark.asyncio
async def test_get_risk_feature(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    tx_id = await _create_transaccion(client, user_id)
    create_resp = await client.post("/api/risk-features", json={"transaction_id": tx_id, "velocity_1m": 1})
    feature_id = create_resp.json()["id"]
    response = await client.get(f"/api/risk-features/{feature_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_risk_feature_not_found(client: AsyncClient) -> None:
    assert (await client.get(f"/api/risk-features/{uuid.uuid4()}")).status_code == 404


@pytest.mark.asyncio
async def test_list_risk_features_by_transaction(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    tx_id = await _create_transaccion(client, user_id)
    await client.post("/api/risk-features", json={"transaction_id": tx_id, "velocity_1m": 2})
    response = await client.get(f"/api/risk-features?transaction_id={tx_id}")
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_update_risk_feature(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    tx_id = await _create_transaccion(client, user_id)
    create_resp = await client.post("/api/risk-features", json={"transaction_id": tx_id, "velocity_1m": 1})
    feature_id = create_resp.json()["id"]
    response = await client.patch(f"/api/risk-features/{feature_id}", json={"velocity_1m": 99})
    assert response.status_code == 200
    assert response.json()["velocity_1m"] == 99


@pytest.mark.asyncio
async def test_delete_risk_feature(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    tx_id = await _create_transaccion(client, user_id)
    create_resp = await client.post("/api/risk-features", json={"transaction_id": tx_id})
    feature_id = create_resp.json()["id"]
    assert (await client.delete(f"/api/risk-features/{feature_id}")).status_code == 204
    assert (await client.get(f"/api/risk-features/{feature_id}")).status_code == 404
