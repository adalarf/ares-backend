from pydantic import BaseModel


class ItemId(BaseModel):
    id: int


class ItemInfo(BaseModel):
    id: int
    name: str
    path: str
    price: int
    rarity: str


class ItemsInfo(BaseModel):
    items: list[ItemInfo]


class ItemShortInfo(BaseModel):
    price: float
    path: str
