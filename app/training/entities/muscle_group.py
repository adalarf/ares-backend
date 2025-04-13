from pydantic import BaseModel


class MuscleGroupResponse(BaseModel):
    id: int
    name: str
    