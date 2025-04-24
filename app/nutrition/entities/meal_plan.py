from pydantic import BaseModel


class MealPlanCreation(BaseModel):
    age: int
    gender: str
    height: float
    weight: float
    # activity_level: str
    goal: str
    restrictions: list[str] | None = None
