from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.users import current_active_user
from src.database import User, get_async_session
from src.profile.schemas import ProfileProductList, ProfileRead
from src.profile.utils import generate_eat_list_products

router = APIRouter()

from fastapi import APIRouter, Depends, HTTPException

from src.eat_list.schemas import EatListCreate
from src.eat_list.service import (
    create_eat_list,
    create_list_product,
    read_eat_list_by_id,
)
from src.product.service import read_products
from src.profile.service import (
    read_profile_info,
    read_profile_list_products,
    read_profile_lists,
)
from src.user_product.service import read_user_products


@router.get("", response_model=ProfileRead)
async def get_profile(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    user_lists = await read_profile_lists(db, user_id=user.id)
    info = await read_profile_info(db, user_id=user.id)
    return {"username": user.username, "info": info, "lists": user_lists}


@router.post("/list", response_model=ProfileProductList)
async def generate_new_eat_list(
    eat_list: EatListCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    # Получаю все продукты, а также info пользователя
    products = await read_products(db)
    liked_products = await read_user_products(db, user_id=user.id, liked=True)
    disliked_products = await read_user_products(db, user_id=user.id, liked=False)
    user_info = await read_profile_info(db, user_id=user.id)
    if not products:
        raise HTTPException(status_code=404, detail="Available products not found")

    if not user_info:
        raise HTTPException(
            status_code=422, detail="Please fill in information about yourself"
        )

    list_products = await generate_eat_list_products(
        products, liked_products, disliked_products, user_info
    )
    if not list_products:
        raise HTTPException(
            status_code=404, detail="Generating products service are not available"
        )

    created_eat_list = await create_eat_list(db, eat_list, user_id=user.id)
    for list_product in list_products:
        await create_list_product(db, created_eat_list.id, list_product)

    list_products = await read_profile_list_products(db, list_id=created_eat_list.id)
    return {"name": created_eat_list.name, "products": list_products}


@router.get("/{list_id}", response_model=ProfileProductList)
async def get_profile_eat_list(
    list_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    exist_list = await read_eat_list_by_id(db, list_id)
    if not exist_list:
        raise HTTPException(status_code=404, detail="Eat list not found")

    if exist_list.user_id != user.id:
        raise HTTPException(status_code=403)

    list_products = await read_profile_list_products(db, list_id=list_id)
    return {"name": exist_list.name, "products": list_products}
