from pydantic import BaseModel
from typing import List

class MealPlanCreation(BaseModel):
    age: int
    gender: str
    height: float
    weight: float
    # activity_level: str
    goal: str
    restrictions: list[str] | None = None


class MealCreate(BaseModel):
    meal: str
    dish: str
    image: str | None = None
    grams: float
    calories: float
    proteins: float
    fats: float
    carbs: float

    class Config:
        from_attributes = True

class MealPlanCreate(BaseModel):
    user_id: int
    meals: List[MealCreate]

    class Config:
        from_attributes = True

class MealRead(MealCreate):
    id: int
    is_eaten: bool

class MealPlanRead(BaseModel):
    id: int
    user_id: int
    total_calories: float
    proteins: float
    fats: float
    carbs: float
    calories_burned: float = 0.0
    calories_eaten: float = 0.0
    proteins_eaten: float = 0.0
    fats_eaten: float = 0.0
    carbs_eaten: float = 0.0
    meals: List[MealRead]

    class Config:
        from_attributes = True
