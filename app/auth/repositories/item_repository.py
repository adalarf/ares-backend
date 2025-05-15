from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.auth.models.item import ItemModel
from sqlalchemy.orm import selectinload
from app.auth.models.user import UserModel


class ItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, item_id: int) -> ItemModel | None:
        query = select(ItemModel).where(ItemModel.id == item_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def add_item_to_user(self, user_id: int, item_id: int) -> None:
        # Используем прямой SQL запрос для вставки в промежуточную таблицу
        await self.db.execute(
            text("""
            INSERT INTO user_items (user_id, item_id)
            VALUES (:user_id, :item_id)
            """),
            {"user_id": user_id, "item_id": item_id}
        )
        await self.db.commit()

    

    async def get_all(self) -> list[ItemModel]:
        query = select(ItemModel)
        result = await self.db.execute(query)
        return result.scalars().all()
        
    async def get_items_by_user_id(self, user_id: int) -> list[ItemModel]:
        query = select(UserModel).options(selectinload(UserModel.items)).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        
        return user.items if user else []
    