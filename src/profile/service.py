from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Currency, EatList, EatListProduct, Product
from src.profile.schemas import ProfileEatList

# async def read_profile_lists(
#     db: AsyncSession, user_id: int
# ) -> list[EatList]:
#     query = (
#         select(EatList)
#         .where(EatList.user_id == user_id)
#     )
#     result = await db.execute(query)
#     return result.scalars().all()


async def read_profile_lists(db: AsyncSession, user_id: int) -> list[ProfileEatList]:
    query = select(EatList).where(EatList.user_id == user_id)
    result = await db.execute(query)
    eat_lists = result.scalars().all()

    for eat_list in eat_lists:
        print("\n\n\n\n\n")
        print(eat_list)
        print("\n\n\n\n\n")

        eat_list_query = select(
            func.sum(EatListProduct.price * EatListProduct.count)
        ).where(EatListProduct.eat_list_id == eat_list.id)
        eat_list.total_price_per_month = await db.scalar(eat_list_query)

        nutrition_fields = [
            "calories",
            "total_fat",
            "total_carb",
            "total_protein",
            "vitamin_d",
            "calcium",
            "iron",
            "potassium",
        ]
        for field in nutrition_fields:
            nutrition_query = (
                select(func.sum(getattr(Product, field) * EatListProduct.count))
                .join(EatListProduct, Product.id == EatListProduct.product_id)
                .where(EatListProduct.eat_list_id == eat_list.id)
            )
            setattr(eat_list, f"{field}_per_month", await db.scalar(nutrition_query))

        currency_query = (
            select(Currency.quote)
            .join(Product, Currency.id == Product.currency_id)
            .join(EatListProduct, Product.id == EatListProduct.product_id)
            .where(EatListProduct.eat_list_id == eat_list.id)
            .distinct()
        )
        eat_list.currency = await db.scalar(currency_query)

        available_query = (
            select(func.bool_and(Product.available))
            .join(EatListProduct, Product.id == EatListProduct.product_id)
            .where(EatListProduct.eat_list_id == eat_list.id)
        )
        eat_list.available = await db.scalar(available_query)

    return eat_lists
