from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.users import current_active_user
from src.database import User, get_async_session
from src.eat_list.schemas import (
    EatListCreate,
    EatListProductCreate,
    EatListProductRead,
    EatListRead,
)
from src.product.service import read_product_by_id

router = APIRouter()

from src.eat_list.service import (
    create_eat_list,
    create_list_product,
    delete_eat_list,
    read_eat_list_by_id,
    read_eat_lists,
    read_list_products,
    read_list_products_by_product_id,
)


@router.get("", response_model=list[EatListRead])
async def get_eat_lists(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)
):
    result = await read_eat_lists(db, skip=skip, limit=limit)
    return result


@router.get("/{list_id}", response_model=EatListRead)
async def get_eat_list_by_id(
    list_id: int, db: AsyncSession = Depends(get_async_session)
):
    result = await read_eat_list_by_id(db, list_id)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Eat list not found")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=EatListRead)
async def create_new_eat_list(
    eat_list: EatListCreate,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
):
    result = await create_eat_list(db, eat_list, user_id=user.id)
    return result


@router.delete("/{list_id}")
async def delete_existing_eat_list(
    list_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    exist_list = await read_eat_list_by_id(db, list_id)
    if not exist_list:
        raise HTTPException(status_code=404, detail="Eat list not found")

    if exist_list.user_id != user.id:
        raise HTTPException(status_code=403)

    await delete_eat_list(db, list_id)
    return {"message": "Eat list deleted successfully"}


# EAT LIST PRODUCT
@router.get("/{list_id}/products", response_model=list[EatListProductRead])
async def get_list_products(
    list_id: int, db: AsyncSession = Depends(get_async_session)
):
    exist_list = await read_eat_list_by_id(db, list_id)
    if exist_list:
        result = await read_list_products(db, list_id)
        return result
    else:
        raise HTTPException(status_code=404, detail="Eat list not found")


@router.post(
    "/{list_id}/products",
    status_code=status.HTTP_201_CREATED,
    response_model=EatListProductRead,
)
async def create_new_list_product(
    list_id: int,
    list_product: EatListProductCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    exist_list = await read_eat_list_by_id(db, list_id)
    if not exist_list:
        raise HTTPException(status_code=404, detail="Eat list not found")

    if exist_list.user_id != user.id:
        raise HTTPException(status_code=403)

    exist_product = await read_product_by_id(db, list_product.product_id)
    if not exist_product:
        raise HTTPException(status_code=404, detail="Product not found")

    already_in_list_product = await read_list_products_by_product_id(
        db, list_id, list_product.product_id
    )
    if already_in_list_product:
        raise HTTPException(status_code=404, detail="This product already in eat list")

    result = await create_list_product(db, list_id, list_product)
    return result
