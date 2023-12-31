from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import EatListProduct, Product, UserProduct
from src.product.schemas import ProductCreate, ProductRead


async def read_products(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[ProductRead]:
    query = select(Product).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def read_product_by_id(db: AsyncSession, id: int) -> ProductRead:
    query = select(Product).where(Product.id == id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_product(db: AsyncSession, product: ProductCreate) -> ProductRead:
    insert_query = insert(Product).values(**product.model_dump()).returning(Product)

    product = await db.execute(insert_query)
    await db.commit()
    return product.scalars().first()


async def delete_product(db: AsyncSession, product_id: int):
    # Удаляем записи из eat_list_product связанные с удаляемым продуктом
    delete_eat_list_products_query = delete(EatListProduct).where(
        EatListProduct.product_id == product_id
    )
    await db.execute(delete_eat_list_products_query)

    # Удаляем записи из user_product связанные с удаляемым продуктом
    delete_user_products_query = delete(UserProduct).where(
        UserProduct.product_id == product_id
    )
    await db.execute(delete_user_products_query)

    # Удаляем сам продукт
    delete_product_query = delete(Product).where(Product.id == product_id)
    await db.execute(delete_product_query)

    await db.commit()
