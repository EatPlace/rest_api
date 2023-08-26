from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.eat_list.schemas import EatListCreate, EatListRead

router = APIRouter()

from src.eat_list.service import create_eat_list, read_eat_list_by_id, read_eat_lists


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
    eat_list: EatListCreate, db: AsyncSession = Depends(get_async_session)
):
    result = await create_eat_list(db, eat_list)
    return result
