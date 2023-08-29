import pytest
from async_asgi_testclient import TestClient
from fastapi import status


async def test_get_products_not_auth(client: TestClient) -> None:
    resp = await client.get("/user_products")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_products(auth_client: TestClient) -> None:
    resp = await auth_client.get("/user_products")
    assert resp.status_code == status.HTTP_200_OK


async def test_get_not_exist_product_not_auth(client: TestClient) -> None:
    resp = await client.get("/user_products/1")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_not_exist_product(auth_client: TestClient) -> None:
    resp = await auth_client.get("/user_products/1")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_not_exist_user_product_not_auth(client: TestClient) -> None:
    resp = await client.delete("/user_products/1")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


async def test_delete_not_exist_product(auth_client: TestClient) -> None:
    resp = await auth_client.delete("/user_products/1")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


async def test_create_user_product_not_auth(client: TestClient, add_product_db) -> None:
    json_data = {
        "like": True,
        "product_id": 1,
        "reason": "Too many sugar",
        "recommend": False,
        "special_name": "My special product name"
    }
    resp = await client.post("/user_products", json=json_data)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


async def test_create_user_product(auth_client: TestClient, add_product_db) -> None:
    json_data = {
        "like": True,
        "product_id": 1,
        "reason": "Too many sugar",
        "recommend": False,
        "special_name": "My special product name"
    }
    resp = await auth_client.post("/user_products", json=json_data)
    resp_json = resp.json()
    resp_json.pop("id", None)
    resp_json.pop("user_id", None)

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp_json == json_data


async def test_get_exist_user_product_not_auth(client: TestClient) -> None:
    resp = await client.get("/user_products/1")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_exist_user_product(auth_client: TestClient) -> None:
    resp = await auth_client.get("/user_products/1")
    assert resp.status_code == status.HTTP_200_OK


async def test_delete_exist_user_product_not_auth(client: TestClient) -> None:
    resp = await client.delete("/user_products/1")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


async def test_delete_exist_product(auth_client: TestClient) -> None:
    resp = await auth_client.delete("/user_products/1")
    assert resp.status_code == status.HTTP_200_OK
    