from sqlalchemy import select
from app.nutrition.models.ingridient import IngredientModel
from sqlalchemy.ext.asyncio import AsyncSession


class IngredientRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_name(self, name: str) -> IngredientModel | None:
        query = select(IngredientModel).where(IngredientModel.name == name)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, name: str) -> IngredientModel:
        ingredient = IngredientModel(
            name=name
        )
        self.db.add(ingredient)
        await self.db.commit()
        await self.db.refresh(ingredient)
        return ingredient
