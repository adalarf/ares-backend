from app.nutrition.models.meal_plan import MealPlanModel
from app.nutrition.models.meal import MealModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class MealPlanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int) -> MealPlanModel:
        plan = MealPlanModel(user_id=user_id)
        self.db.add(plan)
        await self.db.commit()
        await self.db.refresh(plan)
        return plan


    async def update(self, plan: MealPlanModel) -> MealPlanModel:
        self.db.add(plan)
        await self.db.commit()
        await self.db.refresh(plan)
        return plan

    async def get_by_user_id(self, user_id: int) -> MealPlanModel | None:
        query = select(MealPlanModel).options(selectinload(MealPlanModel.meals)
                                              .selectinload(MealModel.dish)).where(MealPlanModel.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().first()
