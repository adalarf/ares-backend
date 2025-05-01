from sqlalchemy import Column, Integer, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class AnswerModel(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    is_right = Column(Boolean, nullable=False, default=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)

    question = relationship("QuestionModel", back_populates="answers")
