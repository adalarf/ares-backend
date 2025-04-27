from app.nutrition.models.meal import MealModel
from sqlalchemy.ext.asyncio import AsyncSession


class MealRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, plan_id: int, dish_id: int, grams: float, proteins: float, fats: float, carbs: float) -> MealModel:
        meal = MealModel(
            plan_id=plan_id,
            dish_id=dish_id,
            grams=grams,
            proteins=proteins,
            fats=fats,
            carbs=carbs
        )
        self.db.add(meal)
        await self.db.commit()
        await self.db.refresh(meal)
        return meal
