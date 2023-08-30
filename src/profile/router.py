from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.users import current_active_user
from src.database import User, get_async_session
from src.profile.schemas import ProfileProductList, ProfileRead

router = APIRouter()

from fastapi import APIRouter, Depends, HTTPException

from src.eat_list.service import read_eat_list_by_id
from src.profile.service import read_profile_list_products, read_profile_lists


@router.get("", response_model=ProfileRead)
async def get_profile(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    user_lists = await read_profile_lists(db, user_id=user.id)
    return {"username": user.username, "lists": user_lists}


@router.get("{list_id}", response_model=ProfileProductList)
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
    return {"name": user.username, "products": list_products}
