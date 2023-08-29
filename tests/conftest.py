import asyncio
from typing import Any, Generator, AsyncGenerator
from src.main import app
from async_asgi_testclient import TestClient
from fastapi import status

import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.main import app
from src.models import Base, Currency, ProductSource, ProductType, Product
from src.database import engine, async_session_maker, get_user_db


# @pytest.fixture(autouse=True, scope="session")
# def run_migrations() -> None:
#     import os

#     print("running migrations..")
#     os.system("alembic upgrade head")


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture
async def auth_client(client: TestClient) -> TestClient:
    # Авторизация пользователя и получение токена
    json_data = {
        "username": "email@fake.com",
        "password": "123456!S",
    }
    response = await client.post(
        "/auth/login",
        data=json_data,
    )
    assert response.status_code == status.HTTP_200_OK
    resp_json = response.json()
    assert "access_token" in resp_json
    assert "token_type" in resp_json
    token = resp_json["access_token"]
    
    # Создание клиента с авторизационным заголовком
    authenticated_client = TestClient(app, headers={"Authorization": f"Bearer {token}"})
    return authenticated_client


@pytest.fixture(autouse=True, scope="session")
async def setup_db():
    async with async_session_maker() as db:
        # Создание и добавление объектов в базу данных
        currency = Currency(id=1, quote="RUB")
        product_source = ProductSource(id=1, name="Yandex lavka", link="http://yandex-lavka.com")
        product_type = ProductType(id=1, name="Delicious")
        
        db.add_all([currency, product_source, product_type])

        await db.commit()
    