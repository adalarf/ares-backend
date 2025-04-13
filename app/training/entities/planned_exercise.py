from pydantic import BaseModel
from typing import Optional


class PlannedExercise(BaseModel):
    id: Optional[int]
    workout_day_id: int
    exercise_id: int


class PlannedExerciseCreation(BaseModel):
    workout_day_id: int
    exercise_id: int


class PlannedExerciseResponse(BaseModel):
    id: int
    workout_day_id: int
    exercise_id: int

    class Config:
        orm_mode = True

