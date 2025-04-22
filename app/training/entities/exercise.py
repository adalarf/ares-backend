from pydantic import BaseModel


class ExerciseCreation(BaseModel):
    name: str
    training_place: str
    muscle_group_id: int
    sets_number_default: int
    repetitions_default: int
    gems_default: int
    expirience_default: int
    expirience_level: str


class ExerciseResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    image: str | None = None
    training_place: str
    muscle_group_id: int
    sets_number_default: int
    repetitions_default: int
    gems_default: int
    expirience_default: int
    expirience_level: str

    class Config:
        orm_mode = True