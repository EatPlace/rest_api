from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UserProduct, EatList
from src.profile.schemas import EatList


async def read_profile_lists(
    db: AsyncSession, user_id: int
) -> list[EatList]:
    query = (
        select(EatList)
        .where(EatList.user_id == user_id)
    )
    result = await db.execute(query)
    return result.scalars().all()

