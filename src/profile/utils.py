import random

from src.eat_list.schemas import EatListProductCreate
from src.product.schemas import ProductRead
from src.profile.schemas import ProfileInfo
from src.user_product.schemas import UserProductRead


def get_DCI_cals_per_days(user_info: ProfileInfo, days=1):
    return (user_info.weight * 10 - user_info.age * 5) * user_info.activity * days


async def generate_eat_list_products(
    available_products: list[ProductRead],
    liked_products: list[UserProductRead],
    disliked_products: list[UserProductRead],
    user_info: ProfileInfo,
) -> list[EatListProductCreate]:
    """
    Должен из списка всех продуктов формировать по какому-то
    разнообразному алгоритму список таких, которые максимально
    близко приблизят к норме калорий в месяц для этого человека

    Примечание: должен учитывать список таких продуктов,
    которые не нравятся пользователю, а также добавлять
    приоритет появления тем, которые лайкнул пользователь
    """
    MAX_CALS_PER_DAY_OVERSUPPLY = 300
    cals_per_day = get_DCI_cals_per_days(user_info, days=1)
    total_days = 30

    # Убираем все непонравившиеся
    disliked_products_ids = {up.product_id for up in disliked_products}
    available_products = [
        product
        for product in available_products
        if product.id not in disliked_products_ids
    ]

    list_products = {}
    for _ in range(total_days):
        # Рассчитайте, сколько калорий осталось для этого дня
        remaining_cals = cals_per_day

        # Создайте список продуктов для этого дня
        tryes = 0
        # Выбирайте случайные продукты, чтобы заполнить остаток калорий
        while remaining_cals > 0:
            product = random.choice(available_products)

            if (product.calories - remaining_cals) < MAX_CALS_PER_DAY_OVERSUPPLY:
                if product.id in list_products:
                    list_products[product.id].count += 1
                else:
                    list_products[product.id] = EatListProductCreate(
                        count=1, price=product.price, product_id=product.id
                    )

                remaining_cals -= product.calories
            else:
                tryes += 1
                if tryes > 10:
                    break

    return [product for product in list_products.values()]
