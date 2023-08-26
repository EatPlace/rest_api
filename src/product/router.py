from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.product.schemas import ProductRead

router = APIRouter()

from src.product.service import read_product_by_id, read_products


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


# @router.post("/client", status_code=status.HTTP_201_CREATED, response_model=Client)
# async def create_new_client(client: ClientCreate):
#     try:
#         created_client = await create_client(client)
#         return created_client
#     except UniqueViolationError as e:
#         raise HTTPException(status_code=400, detail=e.message)


# @router.put("/client/{client_id}", response_model=Client)
# async def update_existing_client(client_id: int, new_client: ClientCreate):
#     exist_client = await read_client_by_id(client_id)
#     if exist_client:
#         return await update_client(client_id, new_client)
#     else:
#         raise HTTPException(status_code=404, detail="Client not found")


# @router.delete("/client/{client_id}")
# async def delete_existing_client(client_id: int):
#     exist_client = await read_client_by_id(client_id)
#     if exist_client:
#         await delete_client(client_id)
#         return {"message": "Client deleted successfully"}
#     else:
#         raise HTTPException(status_code=404, detail="Client not found")
