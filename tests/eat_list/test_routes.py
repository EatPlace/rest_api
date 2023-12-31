import pytest
from async_asgi_testclient import TestClient
from fastapi import status


async def test_get_lists(client: TestClient) -> None:
    resp = await client.get("/eat_lists")
    assert resp.status_code == status.HTTP_200_OK


async def test_get_not_exist_list(client: TestClient) -> None:
    resp = await client.get("/eat_lists/1")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


async def test_get_not_exist_list_product(client: TestClient) -> None:
    resp = await client.get("/eat_lists/1/products")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_not_exist_list_not_auth(client: TestClient) -> None:
    resp = await client.delete("/eat_lists/1")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


async def test_delete_not_exist_list(auth_client: TestClient) -> None:
    resp = await auth_client.delete("/eat_lists/1")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


async def test_create_list_not_auth(client: TestClient) -> None:
    json_data = {
        "name": "Economy set",
    }
    resp = await client.post("/eat_lists", json=json_data)
    resp_json = resp.json()
    resp_json.pop("id", None)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


async def test_create_list(auth_client: TestClient) -> None:
    json_data = {
        "name": "Economy set",
    }
    resp = await auth_client.post("/eat_lists", json=json_data)
    resp_json = resp.json()
    resp_json.pop("user_id", None)
    resp_json.pop("id", None)

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp_json == json_data


async def test_get_list(client: TestClient) -> None:
    resp = await client.get("/eat_lists/1")
    assert resp.status_code == status.HTTP_200_OK


async def test_get_empty_list_products(client: TestClient) -> None:
    resp = await client.get("/eat_lists/1/products")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == []


async def test_create_list_product_not_auth(client: TestClient) -> None:
    json_data = {
        "count": 3,
        "price": 150,
        "product_id": 1
    }
    resp = await client.post("/eat_lists/1/products", json=json_data)
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


async def test_create_list_product(auth_client: TestClient) -> None:
    json_data = {
        "count": 3,
        "price": 150,
        "product_id": 1
    }
    resp = await auth_client.post("/eat_lists/1/products", json=json_data)
    resp_json = resp.json()
    resp_json.pop("eat_list_id", None)
    resp_json.pop("id", None)

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp_json == json_data


async def test_get_list_products(client: TestClient) -> None:
    resp = await client.get("/eat_lists/1/products")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() != []


async def test_delete_list_not_auth(client: TestClient) -> None:
    resp = await client.delete("/eat_lists/1")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


async def test_delete_list(auth_client: TestClient) -> None:
    resp = await auth_client.delete("/eat_lists/1")
    assert resp.status_code == status.HTTP_200_OK
