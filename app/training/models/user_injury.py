from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


user_injury = Table(
    "user_injury",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("muscle_group_id", Integer, ForeignKey("muscle_groups.id"), primary_key=True),
)
