from async_asgi_testclient import TestClient
from fastapi import status


async def test_get_profile_not_auth(client: TestClient) -> None:
    resp = await client.get("/profile")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_empty_profile(auth_client: TestClient) -> None:
    resp = await auth_client.get("/profile")
    assert resp.status_code == status.HTTP_200_OK


async def test_get_profile(auth_client: TestClient, setup_test_data) -> None:
    resp = await auth_client.get("/profile")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()['lists'] != []


async def test_get_profile_empty_products_not_auth(client: TestClient) -> None:
    resp = await client.get("/profile/1")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_profile_empty_products(auth_client: TestClient) -> None:
    resp = await auth_client.get("/profile/1")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


async def test_get_profile_products_not_auth(client: TestClient, setup_test_data) -> None:
    resp = await client.get("/profile/1")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_profile_products(auth_client: TestClient, setup_test_data) -> None:
    resp = await auth_client.get("/profile/1")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()['products'] != []

