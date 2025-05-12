from sqlalchemy import Column, Integer, ForeignKey, Table
from app.database import Base

# Создаем промежуточную таблицу для связи many-to-many между пользователями и предметами
user_item = Table(
    "user_items",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("item_id", Integer, ForeignKey("items.id", ondelete="CASCADE"), primary_key=True)
)
