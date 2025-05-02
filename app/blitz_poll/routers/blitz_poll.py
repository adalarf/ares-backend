from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.auth.services.auth_service import get_current_user
from app.auth.entities.user import User
from app.blitz_poll.services.blitz_service import BlitzService
from app.blitz_poll.entities.blitz_poll import (
    AnswerRequest, 
    QuestionCreate, 
    BlitzPollDetailResponse,
    AnswerResult
)


router = APIRouter()


@router.post("/blitz_poll", response_model=BlitzPollDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_blitz_poll(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    blitz_service = BlitzService(db)
    result, error = await blitz_service.create_blitz_poll(current_user.id)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return result


@router.get("/blitz_poll/{blitz_poll_id}", response_model=BlitzPollDetailResponse, status_code=status.HTTP_200_OK)
async def get_blitz_poll(
    blitz_poll_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    blitz_service = BlitzService(db)
    result, error = await blitz_service.get_blitz_poll_detail(blitz_poll_id, current_user.id)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error
        )
    
    return result


@router.get("/question/{question_id}", status_code=status.HTTP_200_OK)
async def get_question(
    question_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    blitz_service = BlitzService(db)
    result, error = await blitz_service.get_question_detail(question_id)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error
        )
    
    return result


@router.post("/answer", response_model=AnswerResult, status_code=status.HTTP_200_OK)
async def submit_answer(
    answer_request: AnswerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    blitz_service = BlitzService(db)
    result, error = await blitz_service.submit_answer(
        answer_request.blitz_poll_id, 
        answer_request.question_id,
        answer_request.answer_id,
        current_user.id
    )
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return result


@router.post("/question", status_code=status.HTTP_201_CREATED)
async def create_question(
    question_data: QuestionCreate,
    db: AsyncSession = Depends(get_async_session)
):
    blitz_service = BlitzService(db)
    result, error = await blitz_service.create_question(question_data)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return result
