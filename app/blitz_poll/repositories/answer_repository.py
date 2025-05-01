from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.blitz_poll.models.answer import AnswerModel
from typing import Optional, List, Dict


class AnswerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_answer_by_id(self, answer_id: int) -> Optional[AnswerModel]:
        result = await self.db.execute(
            select(AnswerModel).where(AnswerModel.id == answer_id)
        )
        return result.scalar_one_or_none()
        
    async def validate_answer(self, answer_id: int, question_id: int) -> Optional[AnswerModel]:
        result = await self.db.execute(
            select(AnswerModel)
            .where(AnswerModel.id == answer_id)
            .where(AnswerModel.question_id == question_id)
        )
        return result.scalar_one_or_none()
        
    async def create_answers(self, answers_data: List[Dict], question_id: int) -> List[AnswerModel]:
        answers = []
        for answer_data in answers_data:
            answer = AnswerModel(
                text=answer_data.get("text"),
                is_right=answer_data.get("is_right", False),
                question_id=question_id
            )
            self.db.add(answer)
            answers.append(answer)
        
        await self.db.flush()
        return answers