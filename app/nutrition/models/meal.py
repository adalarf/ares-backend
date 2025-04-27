from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class MealModel(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey("meal_plans.id"))
    dish_id = Column(Integer, ForeignKey("dishes.id"))
    grams = Column(Float)
    proteins = Column(Float)
    fats = Column(Float)
    carbs = Column(Float)

    plan = relationship("MealPlanModel", back_populates="meals")
    dish = relationship("DishModel", back_populates="meals")


from app.nutrition.models.meal_plan import MealPlanModel
