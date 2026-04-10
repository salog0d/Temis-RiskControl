import uuid
from datetime import UTC, datetime, timedelta

import pytest
from httpx import AsyncClient


def _future() -> str:
    return (datetime.now(UTC) + timedelta(hours=1)).isoformat()


@pytest.mark.asyncio
async def test_create_token_blacklist(client: AsyncClient) -> None:
    jti = str(uuid.uuid4())
    response = await client.post(
        "/api/token-blacklist",
        json={"token_jti": jti, "expires_at": _future(), "reason": "logout"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["token_jti"] == jti
    assert data["reason"] == "logout"


@pytest.mark.asyncio
async def test_get_token_blacklist_by_id(client: AsyncClient) -> None:
    jti = str(uuid.uuid4())
    create_resp = await client.post("/api/token-blacklist", json={"token_jti": jti, "expires_at": _future()})
    entry_id = create_resp.json()["id"]
    assert (await client.get(f"/api/token-blacklist/{entry_id}")).status_code == 200


@pytest.mark.asyncio
async def test_get_token_blacklist_by_jti(client: AsyncClient) -> None:
    jti = str(uuid.uuid4())
    await client.post("/api/token-blacklist", json={"token_jti": jti, "expires_at": _future()})
    response = await client.get(f"/api/token-blacklist/by-jti/{jti}")
    assert response.status_code == 200
    assert response.json()["token_jti"] == jti


@pytest.mark.asyncio
async def test_get_token_blacklist_not_found(client: AsyncClient) -> None:
    assert (await client.get(f"/api/token-blacklist/{uuid.uuid4()}")).status_code == 404


@pytest.mark.asyncio
async def test_list_token_blacklist(client: AsyncClient) -> None:
    await client.post("/api/token-blacklist", json={"token_jti": str(uuid.uuid4()), "expires_at": _future()})
    await client.post("/api/token-blacklist", json={"token_jti": str(uuid.uuid4()), "expires_at": _future()})
    response = await client.get("/api/token-blacklist")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_delete_token_blacklist(client: AsyncClient) -> None:
    jti = str(uuid.uuid4())
    create_resp = await client.post("/api/token-blacklist", json={"token_jti": jti, "expires_at": _future()})
    entry_id = create_resp.json()["id"]
    assert (await client.delete(f"/api/token-blacklist/{entry_id}")).status_code == 204
    assert (await client.get(f"/api/token-blacklist/{entry_id}")).status_code == 404


@pytest.mark.asyncio
async def test_delete_token_blacklist_not_found(client: AsyncClient) -> None:
    assert (await client.delete(f"/api/token-blacklist/{uuid.uuid4()}")).status_code == 404
