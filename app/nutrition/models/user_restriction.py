from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


user_restriction = Table(
    "user_restriction",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("restriction_id", Integer, ForeignKey("restrictions.id"), primary_key=True),
    extend_existing=True
)