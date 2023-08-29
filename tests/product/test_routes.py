import pytest
from async_asgi_testclient import TestClient
from fastapi import status


async def test_get_products(client: TestClient) -> None:
    resp = await client.get("/products")
    assert resp.status_code == status.HTTP_200_OK


async def test_get_not_exist_product_by_id(client: TestClient) -> None:
    resp = await client.get("/products/1")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_not_exist_product_not_auth(client: TestClient) -> None:
    resp = await client.delete("/products/1")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


async def test_delete_not_exist_product(auth_client: TestClient) -> None:
    resp = await auth_client.delete("/products/1")
    assert resp.status_code == status.HTTP_404_NOT_FOUND

async def test_create_product(client: TestClient) -> None:
    json_data = {
        "available": True,
        "calcium": 20,
        "calories": 150,
        "currency_id": 1,
        "iron": 1,
        "link": "https://lavka.yandex.ru/213/good/marmelad-dolki-limonnye-marmelandiya-udarnica-250-gram",
        "name": "Мармелад Дольки лимонные Мармеландия «Ударница»",
        "potassium": 100,
        "price": 100,
        "source_id": 1,
        "total_carb": 25,
        "total_fat": 5,
        "total_protein": 1,
        "type_id": 1,
        "vitamin_d": 2,
        "weight": 250
    }
    resp = await client.post("/products", json=json_data)
    resp_json = resp.json()
    resp_json.pop("id", None)

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp_json == json_data


async def test_get_exist_product_by_id(client: TestClient) -> None:
    resp = await client.get("/products/1")
    assert resp.status_code == status.HTTP_200_OK


async def test_delete_exist_product_not_auth(client: TestClient) -> None:
    resp = await client.delete("/products/1")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

async def test_delete_exist_product_by_id(auth_client: TestClient) -> None:
    resp = await auth_client.delete("/products/1")
    assert resp.status_code == status.HTTP_200_OK