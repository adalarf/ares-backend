from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.blitz_poll.models.blitz_poll import BlitzPollModel
from app.blitz_poll.models.blitz_question import BlitzQuestionModel
from app.blitz_poll.models.question import QuestionModel
from app.blitz_poll.models.answer import AnswerModel
from typing import List, Optional, Tuple, Dict


class BlitzPollRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_blitz_poll(self, user_id: int) -> BlitzPollModel:
        new_blitz_poll = BlitzPollModel(user_id=user_id)
        self.db.add(new_blitz_poll)
        await self.db.flush()
        return new_blitz_poll

    async def add_questions_to_blitz_poll(self, blitz_poll_id: int, questions: List[QuestionModel]) -> List[BlitzQuestionModel]:
        blitz_questions = []
        
        for question in questions:
            blitz_question = BlitzQuestionModel(
                blitz_poll_id=blitz_poll_id,
                question_id=question.id
            )
            self.db.add(blitz_question)
            blitz_questions.append(blitz_question)
        
        await self.db.flush()
        return blitz_questions

    async def get_blitz_poll_by_id(self, blitz_poll_id: int, user_id: int) -> Optional[BlitzPollModel]:
        result = await self.db.execute(
            select(BlitzPollModel)
            .where(BlitzPollModel.id == blitz_poll_id)
            .where(BlitzPollModel.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_blitz_question(self, blitz_poll_id: int, question_id: int) -> Optional[BlitzQuestionModel]:
        result = await self.db.execute(
            select(BlitzQuestionModel)
            .where(BlitzQuestionModel.blitz_poll_id == blitz_poll_id)
            .where(BlitzQuestionModel.question_id == question_id)
        )
        return result.scalar_one_or_none()

    async def get_blitz_poll_questions_with_answers(self, blitz_poll_id: int) -> List[Tuple[BlitzQuestionModel, QuestionModel, List[AnswerModel]]]:
        result = await self.db.execute(
            select(BlitzQuestionModel, QuestionModel)
            .join(QuestionModel, BlitzQuestionModel.question_id == QuestionModel.id)
            .where(BlitzQuestionModel.blitz_poll_id == blitz_poll_id)
            .order_by(BlitzQuestionModel.id)
        )
        
        blitz_questions_with_data = []
        for blitz_question, question in result:
            answers_result = await self.db.execute(
                select(AnswerModel)
                .where(AnswerModel.question_id == question.id)
            )
            answers = answers_result.scalars().all()
            
            blitz_questions_with_data.append((blitz_question, question, answers))
            
        return blitz_questions_with_data
    
    async def count_total_questions(self, blitz_poll_id: int) -> int:
        result = await self.db.execute(
            select(func.count(BlitzQuestionModel.id))
            .where(BlitzQuestionModel.blitz_poll_id == blitz_poll_id)
        )
        return result.scalar_one()
        
    async def count_answered_questions(self, blitz_poll_id: int) -> int:
        result = await self.db.execute(
            select(func.count(BlitzQuestionModel.id))
            .where(BlitzQuestionModel.blitz_poll_id == blitz_poll_id)
            .where(BlitzQuestionModel.is_answered == True)
        )
        return result.scalar_one()
    
    async def mark_question_as_answered(self, blitz_question: BlitzQuestionModel) -> None:
        blitz_question.is_answered = True
        await self.db.flush()
        
    async def get_poll_statistics(self, blitz_poll_id: int) -> Dict:
        result = await self.db.execute(
            select(
                func.sum(BlitzQuestionModel.gems).label("total_gems"),
                func.sum(BlitzQuestionModel.expirience).label("total_expirience")
            )
            .where(BlitzQuestionModel.blitz_poll_id == blitz_poll_id)
            .where(BlitzQuestionModel.is_answered == True)
        )
        stats = result.one()
        
        result = await self.db.execute(
            select(
                BlitzQuestionModel, 
                AnswerModel
            )
            .join(
                QuestionModel, 
                BlitzQuestionModel.question_id == QuestionModel.id
            )
            .join(
                AnswerModel, 
                (QuestionModel.id == AnswerModel.question_id) & (AnswerModel.is_right == True)
            )
            .where(BlitzQuestionModel.blitz_poll_id == blitz_poll_id)
        )
        correct_answers_count = len(result.all())
        
        total_questions = await self.count_total_questions(blitz_poll_id)
        
        return {
            "total_gems": stats.total_gems or 0,
            "total_expirience": stats.total_expirience or 0,
            "total_questions": total_questions,
            "correct_answers": correct_answers_count,
            "accuracy_percentage": round(correct_answers_count / total_questions * 100, 1) if total_questions > 0 else 0
        }
        
    async def delete_blitz_poll(self, blitz_poll: BlitzPollModel) -> None:
        await self.db.delete(blitz_poll)