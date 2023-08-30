from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Currency, EatList, EatListProduct, Product
from src.profile.schemas import ProfileEatList, ProfileProduct


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


async def read_profile_list_products(
    db: AsyncSession, list_id: int
) -> list[ProfileProduct]:
    query = (
        select(EatListProduct, Product, Currency)
        .join(EatListProduct.product)
        .join(Product.currency)
        .where(EatListProduct.eat_list_id == list_id)
    )
    result = await db.execute(query)
    eat_list_products = result.fetchall()

    profile_products = []

    for eat_list_product, product, currency in eat_list_products:
        profile_product = ProfileProduct(
            id=product.id,
            name=product.name,
            price=eat_list_product.price,
            count=eat_list_product.count,
            calories_per_month=product.calories * eat_list_product.count,
            total_fat_per_month=product.total_fat * eat_list_product.count,
            total_carb_per_month=product.total_carb * eat_list_product.count,
            total_protein_per_month=product.total_protein * eat_list_product.count,
            vitamin_d_per_month=product.vitamin_d * eat_list_product.count,
            calcium_per_month=product.calcium * eat_list_product.count,
            iron_per_month=product.iron * eat_list_product.count,
            potassium_per_month=product.potassium * eat_list_product.count,
            currency=currency.quote,
            available=product.available,
        )
        profile_products.append(profile_product)

    return profile_products
