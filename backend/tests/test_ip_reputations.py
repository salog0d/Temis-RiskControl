import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_ip_reputation(client: AsyncClient) -> None:
    response = await client.post(
        "/api/ip-reputations",
        json={"ip": "1.2.3.4", "risk_score": "0.75", "status": "suspicious", "failed_attempts": 3},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["ip"] == "1.2.3.4"
    assert data["status"] == "suspicious"
    assert data["failed_attempts"] == 3


@pytest.mark.asyncio
async def test_create_ip_reputation_duplicate(client: AsyncClient) -> None:
    await client.post("/api/ip-reputations", json={"ip": "5.5.5.5"})
    response = await client.post("/api/ip-reputations", json={"ip": "5.5.5.5"})
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_ip_reputation(client: AsyncClient) -> None:
    create_resp = await client.post("/api/ip-reputations", json={"ip": "2.3.4.5"})
    entry_id = create_resp.json()["id"]
    assert (await client.get(f"/api/ip-reputations/{entry_id}")).status_code == 200


@pytest.mark.asyncio
async def test_get_ip_reputation_by_ip(client: AsyncClient) -> None:
    await client.post("/api/ip-reputations", json={"ip": "9.9.9.9"})
    response = await client.get("/api/ip-reputations/by-ip/9.9.9.9")
    assert response.status_code == 200
    assert response.json()["ip"] == "9.9.9.9"


@pytest.mark.asyncio
async def test_get_ip_reputation_not_found(client: AsyncClient) -> None:
    assert (await client.get(f"/api/ip-reputations/{uuid.uuid4()}")).status_code == 404


@pytest.mark.asyncio
async def test_list_ip_reputations(client: AsyncClient) -> None:
    await client.post("/api/ip-reputations", json={"ip": "10.0.0.1"})
    await client.post("/api/ip-reputations", json={"ip": "10.0.0.2"})
    response = await client.get("/api/ip-reputations")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_update_ip_reputation(client: AsyncClient) -> None:
    create_resp = await client.post("/api/ip-reputations", json={"ip": "11.0.0.1", "failed_attempts": 0})
    entry_id = create_resp.json()["id"]
    response = await client.patch(f"/api/ip-reputations/{entry_id}", json={"failed_attempts": 5, "status": "blocked"})
    assert response.status_code == 200
    data = response.json()
    assert data["failed_attempts"] == 5
    assert data["status"] == "blocked"


@pytest.mark.asyncio
async def test_delete_ip_reputation(client: AsyncClient) -> None:
    create_resp = await client.post("/api/ip-reputations", json={"ip": "12.0.0.1"})
    entry_id = create_resp.json()["id"]
    assert (await client.delete(f"/api/ip-reputations/{entry_id}")).status_code == 204
    assert (await client.get(f"/api/ip-reputations/{entry_id}")).status_code == 404


@pytest.mark.asyncio
async def test_delete_ip_reputation_not_found(client: AsyncClient) -> None:
    assert (await client.delete(f"/api/ip-reputations/{uuid.uuid4()}")).status_code == 404
