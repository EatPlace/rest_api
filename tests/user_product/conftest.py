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

@pytest.fixture(scope="session")
async def add_product_db():
    async with async_session_maker() as db:
        # Создание и добавление объектов в базу данных
        product = Product(
            id=1,
            available= True,
            calcium = 20,
            calories = 150,
            currency_id = 1,
            iron = 1,
            link = "https://lavka.yandex.ru/213/good/marmelad-dolki-limonnye-marmelandiya-udarnica-250-gram",
            name = "Мармелад Дольки лимонные Мармеландия «Ударница»",
            potassium = 100,
            price = 100,
            source_id = 1,
            total_carb = 25,
            total_fat = 5,
            total_protein = 1,
            type_id = 1,
            vitamin_d = 2,
            weight = 250
        )
        
        db.add_all([product])

        await db.commit()