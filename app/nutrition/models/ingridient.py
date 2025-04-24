from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


class IngredientModel(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    dishes = relationship(
        "DishModel", 
        secondary="dish_ingredient", 
        back_populates="ingredients"
    )
