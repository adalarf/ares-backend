from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class ExerciseModel(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    training_place = Column(String, nullable=False)
    image = Column(String, nullable=True)

    sets_number_default = Column(Integer, nullable=False)
    repetitions_default = Column(Integer, nullable=False)
    gems_default = Column(Integer, nullable=False)
    expirience_default = Column(Integer, nullable=False)
    expirience_level = Column(String, nullable=False)

    muscle_group_id = Column(Integer, ForeignKey("muscle_groups.id", ondelete="CASCADE"), nullable=False)
    # exercise_type_id = Column(Integer, ForeignKey("exercise_types.id", ondelete="CASCADE"), nullable=False)
    
    planned_exercises = relationship("PlannedExerciseModel", back_populates="exercise")
    muscle_group = relationship("MuscleGroupModel", back_populates="exercises")
    # exercise_type = relationship("ExerciseTypeModel", back_populates="exercises")
