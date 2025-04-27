from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.nutrition.models.user_restriction import user_restriction
from app.nutrition.models.dish_restriction import dish_restriction


class RestrictionModel(Base):
    __tablename__ = "restrictions"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    dishes = relationship(
        "DishModel", 
        secondary=dish_restriction,
        back_populates="restrictions",
        overlaps="users,restrictions"
    )
    users = relationship(
        "UserModel", 
        secondary=user_restriction, 
        back_populates="restrictions",
        overlaps="dishes"
    )
