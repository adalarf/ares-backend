from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base


dish_ingredient = Table(
    "dish_ingredient",
    Base.metadata,
    Column("dish_id", Integer, ForeignKey("dishes.id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id"), primary_key=True)
)
