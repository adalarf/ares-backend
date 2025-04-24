from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.auth.models.user import GoalEnum
import enum


class DishCategory(enum.Enum):
    BREAKFAST = "Завтрак"
    LUNCH = "Обед"
    DINNER = "Ужин"
    SNACK = "Перекус"


class DishModel(Base):
    __tablename__ = "dishes"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    calories = Column(Float)
    proteins = Column(Float)
    fats = Column(Float)
    carbs = Column(Float)
    category = Column(Enum(DishCategory))
    goal = Column(String)

    meals = relationship("MealModel", back_populates="dish", cascade="all, delete-orphan")
    ingredients = relationship(
        "IngredientModel", 
        secondary="dish_ingredient",
        back_populates="dishes"
    )
    restrictions = relationship(
        "RestrictionModel", 
        secondary="dish_restriction",
        back_populates="dishes"
    )
