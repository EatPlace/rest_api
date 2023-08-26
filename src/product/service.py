from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Product


async def read_products(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[Product]:
    query = select(Product).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.all()


async def read_product_by_id(db: AsyncSession, id: int) -> Product:
    query = select(Product).where(Product.id == id)
    result = await db.execute(query)
    return result.first()
