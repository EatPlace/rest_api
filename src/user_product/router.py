from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.users import current_active_user
from src.database import User, get_async_session
from src.product.service import read_product_by_id
from src.user_product.schemas import UserProductCreate, UserProductRead

router = APIRouter()

from src.user_product.service import (
    create_user_product,
    delete_user_product,
    read_user_product_by_id,
    read_user_products,
)


@router.get("", response_model=list[UserProductRead])
async def get_user_products(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    user_products = await read_user_products(
        db, user_id=user.id, skip=skip, limit=limit
    )
    return user_products


@router.get("/{product_id}", response_model=UserProductRead)
async def get_user_product_by_id(
    product_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    user_product = await read_user_product_by_id(db, product_id)
    if not user_product:
        raise HTTPException(status_code=404, detail="User product not found")

    if user_product.user_id != user.id:
        raise HTTPException(status_code=403)

    return user_product


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserProductRead)
async def create_new_user_product(
    user_product: UserProductCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    exist_product = await read_product_by_id(db, user_product.product_id)
    if not exist_product:
        raise HTTPException(status_code=404, detail="Product not found")

    created_product = await create_user_product(
        db, user_product=user_product, user_id=user.id
    )
    return created_product


@router.delete("/{product_id}")
async def delete_existing_user_product(
    product_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    exist_product = await read_user_product_by_id(db, product_id)
    if not exist_product:
        raise HTTPException(status_code=404, detail="User product not found")

    if exist_product.user_id != user.id:
        raise HTTPException(status_code=403)

    await delete_user_product(db, product_id)
    return {"message": "Product deleted successfully"}
