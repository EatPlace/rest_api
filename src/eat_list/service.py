from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.eat_list.schemas import EatListCreate, EatListRead
from src.models import EatList


async def read_eat_lists(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[EatListRead]:
    query = select(EatList).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def read_eat_list_by_id(db: AsyncSession, id: int) -> EatListRead:
    query = select(EatList).where(EatList.id == id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_eat_list(db: AsyncSession, eat_list: EatListCreate) -> EatListRead:
    insert_query = insert(EatList).values(**eat_list.model_dump()).returning(EatList)

    eat_list = await db.execute(insert_query)
    await db.commit()
    return eat_list.scalars().first()


# async def delete_eat_list(db: AsyncSession, product_id: int):
#     delete_product_query = delete(Product).where(Product.id == product_id)
#     await db.execute(delete_product_query)
#     await db.commit()
