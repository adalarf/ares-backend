from pydantic import BaseModel
from typing import Optional, List


class WorkoutDay(BaseModel):
    id: Optional[int]
    workout_plan_id: int
    day_of_week: str
    date: Optional[str]


class WorkoutDayCreation(BaseModel):
    id: Optional[int]
    workout_plan_id: int
    day_of_week: str
    date: Optional[str]


class WorkoutDayResponse(BaseModel):
    id: int
    workout_plan_id: int
    day_of_week: str
    date: Optional[str]

    class Config:
        orm_mode = True
