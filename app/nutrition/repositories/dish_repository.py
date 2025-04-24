from sqlalchemy import select
from nutrition.models.dish import DishModel
from sqlalchemy.ext.asyncio import AsyncSession


class DishRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def filter_dishes(self, goal: str, restrictions: list[str]):
        query = select(DishModel).where(
            DishModel.goal == goal,
            DishModel.restrictions.notin_(restrictions)
        )
        result = await self.db.execute(query)

        return result.scalars().all()   
