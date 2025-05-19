from sqlalchemy import select
from app.nutrition.models.dish import DishModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.nutrition.models.restriction import RestrictionModel


class DishRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def filter_dishes(self, goal: str, restrictions: list[str]):
        query = select(DishModel).where(
            DishModel.goal == goal,
        )

        if restrictions:
            query = query.where(~DishModel.restrictions.any(RestrictionModel.name.in_(restrictions)))
        result = await self.db.execute(query)
        return result.scalars().all()   


    async def get_by_name(self, name: str) -> DishModel | None:
        query = select(DishModel).where(DishModel.name == name)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_dish(self, name: str, calories: float, proteins: float, fats: float,
                          carbs: float, category: str, goal: str, ingredients: list[str]) -> DishModel:
        dish = DishModel(
            name=name,
            calories=calories,
            proteins=proteins,
            fats=fats,
            carbs=carbs,
            category=category,
            goal=goal,
            ingredients=ingredients
        )
        self.db.add(dish)
        await self.db.commit()
        await self.db.refresh(dish)
        return dish
