from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.eat_list.schemas import (
    EatListCreate,
    EatListProductCreate,
    EatListProductRead,
    EatListRead,
)
from src.models import EatList, EatListProduct


async def read_eat_lists(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[EatListRead]:
    query = select(EatList).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def read_eat_list_by_id(db: AsyncSession, list_id: int) -> EatListRead:
    query = select(EatList).where(EatList.id == list_id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_eat_list(db: AsyncSession, eat_list: EatListCreate) -> EatListRead:
    insert_query = insert(EatList).values(**eat_list.model_dump()).returning(EatList)

    eat_list = await db.execute(insert_query)
    await db.commit()
    return eat_list.scalars().first()


async def delete_eat_list(db: AsyncSession, eat_list_id: int):
    # Удаляем записи из eat_list_product связанные с удаляемым продуктом
    delete_eat_list_products_query = delete(EatListProduct).where(
        EatListProduct.eat_list_id == eat_list_id
    )
    await db.execute(delete_eat_list_products_query)

    delete_product_query = delete(EatList).where(EatList.id == eat_list_id)
    await db.execute(delete_product_query)

    await db.commit()


# EAT LIST PRODUCT
async def read_list_products(
    db: AsyncSession, list_id: int
) -> list[EatListProductRead]:
    query = select(EatListProduct).where(EatListProduct.eat_list_id == list_id)
    result = await db.execute(query)
    return result.scalars().all()


async def read_list_products_by_product_id(
    db: AsyncSession, list_id: int, product_id: int
) -> list[EatListProductRead]:
    query = select(EatListProduct).where(
        (EatListProduct.eat_list_id == list_id)
        & (EatListProduct.product_id == product_id)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def create_list_product(
    db: AsyncSession, list_id: int, list_product: EatListProductCreate
) -> list[EatListProductRead]:
    insert_query = (
        insert(EatListProduct)
        .values(**list_product.model_dump(), eat_list_id=list_id)
        .returning(EatListProduct)
    )

    list_product = await db.execute(insert_query)
    await db.commit()
    return list_product.scalars().first()
