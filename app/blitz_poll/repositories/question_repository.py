from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.blitz_poll.models.question import QuestionModel
from app.blitz_poll.models.answer import AnswerModel
from typing import List, Optional, Dict


class QuestionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_question_by_id(self, question_id: int) -> Optional[QuestionModel]:
        result = await self.db.execute(
            select(QuestionModel).where(QuestionModel.id == question_id)
        )
        return result.scalar_one_or_none()

    async def get_random_questions(self, limit: int = 10) -> List[QuestionModel]:
        query = select(QuestionModel).order_by(func.random()).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_answers_for_question(self, question_id: int) -> List[AnswerModel]:
        query = select(AnswerModel).where(AnswerModel.question_id == question_id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def create_question(self, text: str) -> QuestionModel:
        question = QuestionModel(text=text)
        self.db.add(question)
        await self.db.flush()
        return question
