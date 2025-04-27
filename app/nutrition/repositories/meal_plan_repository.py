from app.nutrition.models.meal_plan import MealPlanModel
from sqlalchemy.ext.asyncio import AsyncSession


class MealPlanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int) -> MealPlanModel:
        plan = MealPlanModel(user_id=user_id)
        self.db.add(plan)
        await self.db.commit()
        await self.db.refresh(plan)
        return plan
