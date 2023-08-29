from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.users import current_active_user
from src.database import User, get_async_session
from src.profile.schemas import ProfileRead

router = APIRouter()

from src.profile.service import read_profile_lists


@router.get("", response_model=ProfileRead)
async def get_profile(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    user_lists = await read_profile_lists(db, user_id=user.id)
    return {"username": user.username, "lists": user_lists}
