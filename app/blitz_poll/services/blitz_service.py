from app.blitz_poll.repositories.blitz_poll_repository import BlitzPollRepository
from app.blitz_poll.repositories.question_repository import QuestionRepository
from app.blitz_poll.repositories.answer_repository import AnswerRepository
from app.auth.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.blitz_poll.entities.blitz_poll import AnswerResult, QuestionCreate
from typing import List, Dict, Optional, Tuple


class BlitzService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.blitz_poll_repo = BlitzPollRepository(db)
        self.question_repo = QuestionRepository(db)
        self.answer_repo = AnswerRepository(db)
        self.user_repo = UserRepository(db)
    
    async def get_questions(self, limit: int = 10):
        questions = await self.question_repo.get_random_questions(limit)
        return questions
    
    async def create_blitz_poll(self, user_id: int, question_count: int = 10):
        questions = await self.get_questions(question_count)
        
        if len(questions) < question_count:
            return None, f"Недостаточно вопросов в базе данных. Требуется {question_count}, найдено {len(questions)}"

        blitz_poll = await self.blitz_poll_repo.create_blitz_poll(user_id)
        blitz_questions = await self.blitz_poll_repo.add_questions_to_blitz_poll(blitz_poll.id, questions)
        
        await self.db.commit()
        
        return {
            "blitz_poll_id": blitz_poll.id,
            "questions_count": len(blitz_questions)
        }, None
    
    async def get_blitz_poll_detail(self, blitz_poll_id: int, user_id: int):
        blitz_poll = await self.blitz_poll_repo.get_blitz_poll_by_id(blitz_poll_id, user_id)
        if not blitz_poll:
            return None, "Блиц-опрос не найден или вы не имеете к нему доступа"
        
        questions_with_answers = await self.blitz_poll_repo.get_blitz_poll_questions_with_answers(blitz_poll_id)
        
        questions_data = {}
        for blitz_question, question, answers in questions_with_answers:
            if question.id not in questions_data:
                questions_data[question.id] = {
                    "question_id": question.id,
                    "text": question.text,
                    "answers": []
                }
            
            for answer in answers:
                questions_data[question.id]["answers"].append({
                    "answer_id": answer.id,
                    "text": answer.text,
                    "is_right": answer.is_right
                })
        
        return {
            "blitz_poll_id": blitz_poll.id,
            "user_id": blitz_poll.user_id,
            "questions": list(questions_data.values())
        }, None
    
    async def get_question_detail(self, question_id: int):
        question = await self.question_repo.get_question_by_id(question_id)
        if not question:
            return None, "Вопрос не найден"
        
        answers = await self.question_repo.get_answers_for_question(question_id)
        
        answers_data = [
            {
                "id": answer.id,
                "text": answer.text
            }
            for answer in answers
        ]
        
        return {
            "question_id": question.id,
            "text": question.text,
            "answers": answers_data
        }, None
    
    async def submit_answer(self, blitz_poll_id: int, question_id: int, answer_id: int, user_id: int) -> Tuple[Optional[AnswerResult], Optional[str]]:
        try:
            blitz_poll = await self.blitz_poll_repo.get_blitz_poll_by_id(blitz_poll_id, user_id)
            if not blitz_poll:
                return None, "Блиц-опрос не найден или вы не имеете к нему доступа"
            
            blitz_question = await self.blitz_poll_repo.get_blitz_question(blitz_poll_id, question_id)
            if not blitz_question:
                return None, "Вопрос не найден в данном блиц-опросе"
            
            if blitz_question.is_answered:
                return None, "Вы уже ответили на этот вопрос"
            
            answer = await self.answer_repo.validate_answer(answer_id, question_id)
            if not answer:
                return None, "Ответ не найден или не соответствует указанному вопросу"
            
            is_correct = answer.is_right
            gems_earned = 0
            expirience_earned = 0
            
            if is_correct:
                gems_earned = blitz_question.gems
                expirience_earned = blitz_question.expirience
                await self.user_repo.add_gems_and_experience_blitz(user_id, gems_earned, expirience_earned)
            
            await self.blitz_poll_repo.mark_question_as_answered(blitz_question)
            
            total_questions = await self.blitz_poll_repo.count_total_questions(blitz_poll_id)
            answered_questions = await self.blitz_poll_repo.count_answered_questions(blitz_poll_id)
            
            answer_result = AnswerResult(
                is_correct=is_correct,
                gems_earned=gems_earned,
                expirience_earned=expirience_earned,
                poll_completed=False
            )
            
            if answered_questions >= total_questions:
                poll_stats = await self.blitz_poll_repo.get_poll_statistics(blitz_poll_id)
                
                answer_result.poll_completed = True
                answer_result.poll_stats = poll_stats
                
                await self.blitz_poll_repo.delete_blitz_poll(blitz_poll)
            else:
                answer_result.progress = {
                    "answered": answered_questions,
                    "total": total_questions,
                    "remaining": total_questions - answered_questions
                }
            
            await self.db.commit()
            
            return answer_result, None
                
        except Exception as e:
            await self.db.rollback()
            return None, f"Ошибка при обработке ответа: {str(e)}"
    
    async def create_question(self, question_data: QuestionCreate) -> Tuple[Optional[Dict], Optional[str]]:
        try:
            question = await self.question_repo.create_question(question_data.text)
            answers_data = [
                {
                    "text": answer.text,
                    "is_right": answer.is_right
                } for answer in question_data.answers
            ]
            
            answers = await self.answer_repo.create_answers(answers_data, question.id)
            answers_data = [{
                "id": answer.id,
                "text": answer.text,
                "is_right": answer.is_right
            } for answer in answers]
            
            result = {
                "id": question.id,
                "text": question.text,
                "answers": answers_data
            }
            
            await self.db.commit()
            return result, None
            
        except Exception as e:
            await self.db.rollback()
            return None, f"Ошибка при создании вопроса: {str(e)}"
