from pydantic import BaseModel, validator
from typing import List, Optional


class AnswerBase(BaseModel):
    text: str
    is_right: bool = False


class AnswerCreate(AnswerBase):
    pass


class AnswerResponse(AnswerBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True


class QuestionBase(BaseModel):
    text: str
    gems: int = 0
    expirience: int = 0


class AnswerCreateItem(BaseModel):
    text: str
    is_right: bool = False


class QuestionCreate(BaseModel):
    text: str
    answers: List[AnswerCreateItem]
    
    @validator('answers')
    def validate_answers(cls, v):
        if len(v) < 2:
            raise ValueError('Вопрос должен иметь минимум два варианта ответа')
            
        right_answers = [answer for answer in v if answer.is_right]
        if len(right_answers) != 1:
            raise ValueError('Вопрос должен иметь ровно один правильный ответ')
            
        return v


class QuestionResponse(QuestionBase):
    id: int
    answers: List[AnswerResponse]

    class Config:
        orm_mode = True


class BlitzQuestionBase(BaseModel):
    question_id: int
    gems: int = 0
    expirience: int = 0
    is_answered: bool = False


class BlitzQuestionCreate(BlitzQuestionBase):
    pass


class BlitzQuestionResponse(BlitzQuestionBase):
    id: int
    blitz_poll_id: int

    class Config:
        orm_mode = True


class BlitzPollBase(BaseModel):
    user_id: int


class BlitzPollCreate(BlitzPollBase):
    pass


class BlitzPollResponse(BlitzPollBase):
    id: int
    questions: List[QuestionResponse]

    class Config:
        orm_mode = True


class AnswerRequest(BaseModel):
    blitz_poll_id: int
    question_id: int
    answer_id: int


class AnswerResult(BaseModel):
    is_correct: bool
    gems_earned: int
    expirience_earned: int
    poll_completed: bool
    progress: Optional[dict] = None
    poll_stats: Optional[dict] = None