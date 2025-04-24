from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class RestrictionModel(Base):
    __tablename__ = "restrictions"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    dishes = relationship(
        "DishModel", 
        secondary="dish_restriction",
        back_populates="restrictions"
    )
    users = relationship(
        "UserModel", 
        secondary="user_restriction", 
        back_populates="restrictions"
    )
