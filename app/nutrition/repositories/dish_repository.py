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
    
    
    async def get_all_restrictions(self):
        query = select(RestrictionModel)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    
    async def add_dish_restrictions(self, dish_id: int, restriction_names: list[str]) -> DishModel:
        # Используем selectinload для явной загрузки связи restrictions вместе с блюдом
        from sqlalchemy.orm import selectinload
        query = select(DishModel).options(selectinload(DishModel.restrictions)).where(DishModel.id == dish_id)
        result = await self.db.execute(query)
        dish = result.scalar_one_or_none()
        
        if not dish:
            raise ValueError(f"Блюдо с ID {dish_id} не найдено")

        query = select(RestrictionModel).where(RestrictionModel.name.in_(restriction_names))
        result = await self.db.execute(query)
        restrictions = result.scalars().all()
        
        found_restriction_names = {r.name for r in restrictions}
        missing_names = set(restriction_names) - found_restriction_names
        
        if missing_names:
            raise ValueError(f"Ограничения не найдены: {', '.join(missing_names)}")
        
        # Теперь dish.restrictions уже загружены, так что это работает без проблем
        existing_restriction_ids = {r.id for r in dish.restrictions}
        for restriction in restrictions:
            if restriction.id not in existing_restriction_ids:
                dish.restrictions.append(restriction)
        
        await self.db.commit()
        await self.db.refresh(dish)
        
        return dish
