from pydantic import BaseModel
from typing import Optional


class RandomExerciseCreation(BaseModel):
    sets_number: int
    repetitions: int
    gems: int
    expirience:int 
    exercise_id:int
    user_id: int
    calories: float


class RandomExerciseInfo(BaseModel):
    id: int
    exercise_id: int
    sets_number: int
    repetitions: int
    gems: int
    expirience: int
    calories: float
    name: str
    image: Optional[str] = None
