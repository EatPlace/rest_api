import uuid

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UserProduct
from src.user_product.schemas import UserProductCreate, UserProductRead


async def read_user_products(
    db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
) -> list[UserProductRead]:
    query = (
        select(UserProduct)
        .where(UserProduct.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def read_user_product_by_id(db: AsyncSession, id: int) -> UserProductRead:
    query = select(UserProduct).where(UserProduct.id == id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_user_product(
    db: AsyncSession, user_product: UserProductCreate, user_id: uuid.UUID
) -> UserProductRead:
    insert_query = (
        insert(UserProduct)
        .values(**user_product.model_dump(), user_id=user_id)
        .returning(UserProduct)
    )

    user_product = await db.execute(insert_query)
    await db.commit()
    return user_product.scalars().first()


async def delete_user_product(db: AsyncSession, user_product_id: int):
    # Удаляем записи из eat_list_product связанные с удаляемым продуктом
    delete_user_products_query = delete(UserProduct).where(
        UserProduct.id == user_product_id
    )
    await db.execute(delete_user_products_query)

    await db.commit()
