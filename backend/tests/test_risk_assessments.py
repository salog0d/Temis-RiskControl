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
async def test_create_risk_assessment(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    tx_id = await _create_transaccion(client, user_id)
    response = await client.post(
        "/api/risk-assessments",
        json={"transaction_id": tx_id, "risk_score": "0.85", "risk_level": "high", "decision": "block"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["risk_level"] == "high"
    assert data["decision"] == "block"


@pytest.mark.asyncio
async def test_get_risk_assessment(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    tx_id = await _create_transaccion(client, user_id)
    create_resp = await client.post("/api/risk-assessments", json={"transaction_id": tx_id, "decision": "approve"})
    assessment_id = create_resp.json()["id"]
    response = await client.get(f"/api/risk-assessments/{assessment_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_risk_assessment_not_found(client: AsyncClient) -> None:
    assert (await client.get(f"/api/risk-assessments/{uuid.uuid4()}")).status_code == 404


@pytest.mark.asyncio
async def test_list_risk_assessments_by_transaction(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    tx_id = await _create_transaccion(client, user_id)
    await client.post("/api/risk-assessments", json={"transaction_id": tx_id, "decision": "approve"})
    response = await client.get(f"/api/risk-assessments?transaction_id={tx_id}")
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_update_risk_assessment(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    tx_id = await _create_transaccion(client, user_id)
    create_resp = await client.post("/api/risk-assessments", json={"transaction_id": tx_id, "decision": "review"})
    assessment_id = create_resp.json()["id"]
    response = await client.patch(f"/api/risk-assessments/{assessment_id}", json={"decision": "block"})
    assert response.status_code == 200
    assert response.json()["decision"] == "block"


@pytest.mark.asyncio
async def test_delete_risk_assessment(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    tx_id = await _create_transaccion(client, user_id)
    create_resp = await client.post("/api/risk-assessments", json={"transaction_id": tx_id})
    assessment_id = create_resp.json()["id"]
    assert (await client.delete(f"/api/risk-assessments/{assessment_id}")).status_code == 204
    assert (await client.get(f"/api/risk-assessments/{assessment_id}")).status_code == 404
