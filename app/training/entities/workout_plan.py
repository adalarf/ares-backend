from pydantic import BaseModel
from typing import List, Optional


class WorkoutPlan(BaseModel):
    id: Optional[int]
    user_id: int
    training_level: str
    goal: str
    training_place: str


class WorkoutPlanCreation(BaseModel):
    training_level: str
    goal: str
    training_place: str


class WorkoutPlanResponse(BaseModel):
    id: int
    user_id: int
    training_level: str
    goal: str
    training_place: str

    class Config:
        orm_mode = True


class ExerciseInfo(BaseModel):
    exercise_id: int
    workout_day_id: int
    sets_number: int
    repetitions: int
    gems: int
    expirience: int
    name: str
    image: Optional[str] = None


class WorkoutDayInfo(BaseModel):
    day_of_week: str
    date: Optional[str]
    image: Optional[str] = None
    muscle_group: str
    exercises: List[ExerciseInfo]


class WeeklyWorkoutPlanResponse(BaseModel):
    workout_plan_id: int
    user_id: int
    days: List[WorkoutDayInfo]

    class Config:
        orm_mode = True

