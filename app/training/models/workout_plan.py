from sqlalchemy import Column, Integer, ForeignKey, Date
from app.database import Base
from sqlalchemy.orm import relationship


class WorkoutPlanModel(Base):
    __tablename__ = "workout_plan"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    week_start_date = Column(Date, nullable=False)
    week_end_date = Column(Date, nullable=False)

    user = relationship("UserModel", back_populates="workout_plans")
    workout_days = relationship("WorkoutDayModel", back_populates="workout_plan", cascade="all, delete")