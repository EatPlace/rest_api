import pytest

from src.models import EatList, EatListProduct
from src.database import async_session_maker
from async_asgi_testclient import TestClient
from src.eat_list.service import delete_eat_list


@pytest.fixture(scope="function")
async def setup_test_data(auth_client: TestClient):
    id_resp = await auth_client.get('/authenticated-route')
    user_id = id_resp.json()['message']

    async with async_session_maker() as db:
        eat_list = EatList(id=1, name="Business", user_id=user_id)
        product = EatListProduct(price=500, count=1, eat_list_id=1, product_id=1)
        
        db.add_all([eat_list, product])
        await db.commit()
        
    yield
    
    # После завершения тестов удаляем тестовые данные
    async with async_session_maker() as db:
        await delete_eat_list(db, eat_list.id)
        await db.commit()