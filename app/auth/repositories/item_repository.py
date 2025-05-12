from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.auth.models.item import ItemModel


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
            """
            INSERT INTO user_items (user_id, item_id)
            VALUES (:user_id, :item_id)
            """,
            {"user_id": user_id, "item_id": item_id}
        )
        await self.db.commit()