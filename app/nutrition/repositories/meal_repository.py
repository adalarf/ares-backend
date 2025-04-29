from app.nutrition.models.meal import MealModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload


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


    async def make_eaten(self, id: int):
        query = update(MealModel).where(MealModel.id == id).values(is_eaten=True)
        await self.db.execute(query)
        await self.db.commit()

    
    async def get_by_id(self, id: int) -> MealModel | None:
        query = select(MealModel).options(selectinload(MealModel.dish)).where(MealModel.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    