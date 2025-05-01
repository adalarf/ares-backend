from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class BlitzQuestionModel(Base):
    __tablename__ = "blitz_questions"

    id = Column(Integer, primary_key=True, index=True)
    gems = Column(Integer, nullable=False, default=1)
    expirience = Column(Integer, nullable=False, default=1)
    is_answered = Column(Boolean, default=False)
    
    blitz_poll_id = Column(Integer, ForeignKey("blitz_polls.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)

    blitz_poll = relationship("BlitzPollModel", back_populates="blitz_questions")
    question = relationship("QuestionModel", back_populates="blitz_questions")
