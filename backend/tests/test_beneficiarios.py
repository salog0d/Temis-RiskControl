import uuid

import pytest
from httpx import AsyncClient


async def _create_usuario(client: AsyncClient) -> str:
    resp = await client.post("/api/usuarios", json={"email": f"{uuid.uuid4()}@example.com"})
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_create_beneficiario(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    response = await client.post(
        "/api/beneficiarios",
        json={"user_id": user_id, "account_number": "001122334455", "bank_name": "BBVA"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user_id
    assert data["account_number"] == "001122334455"
    assert data["bank_name"] == "BBVA"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_beneficiario(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post(
        "/api/beneficiarios",
        json={"user_id": user_id, "account_number": "999888777", "bank_name": "Banamex"},
    )
    beneficiario_id = create_resp.json()["id"]

    response = await client.get(f"/api/beneficiarios/{beneficiario_id}")
    assert response.status_code == 200
    assert response.json()["bank_name"] == "Banamex"


@pytest.mark.asyncio
async def test_get_beneficiario_not_found(client: AsyncClient) -> None:
    response = await client.get(f"/api/beneficiarios/{uuid.uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_beneficiarios(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    await client.post("/api/beneficiarios", json={"user_id": user_id, "account_number": "111", "bank_name": "BBVA"})
    await client.post("/api/beneficiarios", json={"user_id": user_id, "account_number": "222", "bank_name": "HSBC"})

    response = await client.get("/api/beneficiarios")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_list_beneficiarios_filtered_by_user(client: AsyncClient) -> None:
    user_a = await _create_usuario(client)
    user_b = await _create_usuario(client)
    await client.post("/api/beneficiarios", json={"user_id": user_a, "account_number": "111", "bank_name": "BBVA"})
    await client.post("/api/beneficiarios", json={"user_id": user_b, "account_number": "222", "bank_name": "HSBC"})

    response = await client.get(f"/api/beneficiarios?user_id={user_a}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == user_a


@pytest.mark.asyncio
async def test_update_beneficiario(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post(
        "/api/beneficiarios",
        json={"user_id": user_id, "account_number": "000", "bank_name": "OldBank"},
    )
    beneficiario_id = create_resp.json()["id"]

    response = await client.patch(
        f"/api/beneficiarios/{beneficiario_id}",
        json={"account_number": "999", "bank_name": "NewBank"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["account_number"] == "999"
    assert data["bank_name"] == "NewBank"


@pytest.mark.asyncio
async def test_update_beneficiario_not_found(client: AsyncClient) -> None:
    response = await client.patch(f"/api/beneficiarios/{uuid.uuid4()}", json={"bank_name": "X"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_beneficiario(client: AsyncClient) -> None:
    user_id = await _create_usuario(client)
    create_resp = await client.post(
        "/api/beneficiarios",
        json={"user_id": user_id, "account_number": "DEL001", "bank_name": "DeleteBank"},
    )
    beneficiario_id = create_resp.json()["id"]

    response = await client.delete(f"/api/beneficiarios/{beneficiario_id}")
    assert response.status_code == 204

    get_resp = await client.get(f"/api/beneficiarios/{beneficiario_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_beneficiario_not_found(client: AsyncClient) -> None:
    response = await client.delete(f"/api/beneficiarios/{uuid.uuid4()}")
    assert response.status_code == 404
