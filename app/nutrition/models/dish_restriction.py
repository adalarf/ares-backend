from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


dish_restriction = Table(
    "dish_restriction",
    Base.metadata,
    Column("dish_id", Integer, ForeignKey("dishes.id"), primary_key=True),
    Column("restriction_id", Integer, ForeignKey("restrictions.id"), primary_key=True),
    extend_existing=True
)