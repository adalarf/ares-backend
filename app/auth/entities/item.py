from pydantic import BaseModel


class ItemId(BaseModel):
    id: int
