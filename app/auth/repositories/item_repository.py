from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.auth.models.item import ItemModel
from sqlalchemy.orm import selectinload
from app.auth.models.user import UserModel
from app.auth.entities.item import ItemShortInfo


class ItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, item_id: int) -> ItemModel | None:
        query = select(ItemModel.price, ItemModel.path).where(ItemModel.id == item_id)
        result = await self.db.execute(query)
        item = result.first()
        if item:
            return ItemShortInfo(price=item[0], path=item[1])
        return None

    async def add_item_to_user(self, user_id: int, item_id: int) -> None:
        await self.db.execute(
            text("""
            INSERT INTO user_items (user_id, item_id)
            VALUES (:user_id, :item_id)
            """),
            {"user_id": user_id, "item_id": item_id}
        )
        await self.db.commit()

    

    async def get_all(self) -> list[ItemModel]:
        query = select(ItemModel.id, ItemModel.name, ItemModel.path, ItemModel.price, ItemModel.rarity)
        result = await self.db.execute(query)
        return result.all()
        
    async def get_items_by_user_id(self, user_id: int) -> list[tuple]:
        query = (
            select(ItemModel.id, ItemModel.name, ItemModel.path, ItemModel.price, ItemModel.rarity)
            .join(UserModel.items)
            .where(UserModel.id == user_id)
        )
        result = await self.db.execute(query)
        return result.all()
    