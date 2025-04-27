from pydantic import BaseModel
from typing import List


class DishCreation(BaseModel):
    name: str
    calories: float
    proteins: float
    fats: float
    carbs: float
    category: str
    goal: str
    ingredients: list[str] | None = None


class DishesCreation(BaseModel):
    dishes: List[DishCreation]
