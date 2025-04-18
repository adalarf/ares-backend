from pydantic import BaseModel
from typing import Optional

class MuscleGroupResponse(BaseModel):
    id: int
    name: str
    image: Optional[str] = None

    class Config:
        orm_mode = True
