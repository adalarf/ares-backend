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
    intensity: str
    kg50_calories: float | None = None
    kg60_calories: float | None = None
    kg70_calories: float | None = None
    kg80_calories: float | None = None
    kg90_calories: float | None = None
    kg100_calories: float | None = None



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
    intensity: str | None = None
    kg50_calories: float | None = None
    kg60_calories: float | None = None
    kg70_calories: float | None = None
    kg80_calories: float | None = None
    kg90_calories: float | None = None
    kg100_calories: float | None = None

    class Config:
        orm_mode = True