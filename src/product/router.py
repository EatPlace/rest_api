from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.users import current_active_user
from src.database import User, get_async_session
from src.product.schemas import ProductCreate, ProductRead

router = APIRouter()

from src.product.service import (
    create_product,
    delete_product,
    read_product_by_id,
    read_products,
)


@router.get("", response_model=list[ProductRead])
async def get_products(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)
):
    products = await read_products(db, skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=ProductRead)
async def get_product_by_id(
    product_id: int, db: AsyncSession = Depends(get_async_session)
):
    product = await read_product_by_id(db, product_id)
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ProductRead)
async def create_new_product(
    product: ProductCreate, db: AsyncSession = Depends(get_async_session)
):
    created_product = await create_product(db, product)
    return created_product


# @router.put("/client/{client_id}", response_model=Client)
# async def update_existing_client(client_id: int, new_client: ClientCreate):
#     exist_client = await read_client_by_id(client_id)
#     if exist_client:
#         return await update_client(client_id, new_client)
#     else:
#         raise HTTPException(status_code=404, detail="Client not found")


@router.delete("/{product_id}")
async def delete_existing_product(
    product_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    exist_product = await read_product_by_id(db, product_id)
    if exist_product:
        await delete_product(db, product_id)
        return {"message": "Product deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")
