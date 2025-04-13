from pydantic import BaseModel
from typing import Optional


class ExerciseCreation(BaseModel):
    name: str
    sets_number: int
    repetitions: int
    training_place: str
    gems: int
    expirience_level: str
    muscle_group_id: int


class ExerciseResponse(BaseModel):
    id: int
    name: str
    sets_number: int
    repetitions: int
    training_place: str
    gems: int
    expirience_level: str
    muscle_group_id: int

    class Config:
        orm_mode = True