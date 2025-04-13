from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ExerciseTypeModel(Base):
    __tablename__ = "exercise_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)

    exercises = relationship("ExerciseModel", back_populates="exercise_type")
