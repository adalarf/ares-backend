from pydantic import BaseModel
from typing import Optional


class RandomExerciseCreation(BaseModel):
    sets_number: int
    repetitions: int
    gems: int
    expirience:int 
    exercise_id:int
    user_id: int


class RandomExerciseInfo(BaseModel):
    exercise_id: int
    sets_number: int
    repetitions: int
    gems: int
    expirience: int
    name: str
    image: Optional[str] = None
