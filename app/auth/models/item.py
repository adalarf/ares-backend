from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
from app.auth.models.user_item import user_item


class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    path = Column(String, nullable=True)
    price = Column(String, nullable=False)
    rarity = Column(String, nullable=True)
    
    users = relationship(
        "UserModel",
        secondary=user_item,
        back_populates="items"
    )
