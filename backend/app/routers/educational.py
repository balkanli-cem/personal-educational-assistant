from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime

from ..models.database import get_db
from ..models.user import User
from ..models.learning_session import LearningSession
from ..models.quiz import QuizQuestion, QuizResponse
from ..models.learning_progress import LearningProgress
from ..schemas.educational import (
    LearningSessionCreate, LearningSessionResponse,
    QuizQuestionCreate, QuizQuestionResponse,
    QuizResponseCreate, QuizResponseResponse
)
from .auth import get_current_user

router = APIRouter()

@router.post("/session", response_model=LearningSessionResponse)
async def create_learning_session(
    session_data: LearningSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new learning session"""
    db_session = LearningSession(
        user_id=current_user.id,
        **session_data.dict()
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/sessions", response_model=List[LearningSessionResponse])
async def get_user_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all learning sessions for current user"""
    sessions = db.query(LearningSession).filter(
        LearningSession.user_id == current_user.id
    ).order_by(LearningSession.created_at.desc()).all()
    return sessions

@router.get("/sessions/{session_id}", response_model=LearningSessionResponse)
async def get_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific learning session"""
    session = db.query(LearningSession).filter(
        LearningSession.id == session_id,
        LearningSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return session

@router.post("/quiz/question", response_model=QuizQuestionResponse)
async def create_quiz_question(
    question_data: QuizQuestionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new quiz question"""
    # Verify the session belongs to the user
    session = db.query(LearningSession).filter(
        LearningSession.id == question_data.session_id,
        LearningSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    db_question = QuizQuestion(**question_data.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.post("/quiz/response", response_model=QuizResponseResponse)
async def submit_quiz_response(
    response_data: QuizResponseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit a quiz response"""
    # Get the question
    question = db.query(QuizQuestion).filter(
        QuizQuestion.id == response_data.question_id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Check if answer is correct
    is_correct = response_data.selected_answer == question.correct_answer
    
    # Create response
    db_response = QuizResponse(
        question_id=response_data.question_id,
        user_id=current_user.id,
        selected_answer=response_data.selected_answer,
        is_correct=is_correct,
        time_taken=response_data.time_taken
    )
    db.add(db_response)
    
    # Update learning progress
    progress = db.query(LearningProgress).filter(
        LearningProgress.user_id == current_user.id,
        LearningProgress.topic == question.session.topic
    ).first()
    
    if not progress:
        progress = LearningProgress(
            user_id=current_user.id,
            topic=question.session.topic,
            mastery_level=0.0,
            total_sessions=0,
            correct_answers=0,
            total_questions=0
        )
        db.add(progress)
    
    # Update progress statistics
    progress.total_questions += 1
    if is_correct:
        progress.correct_answers += 1
    
    # Calculate mastery level (simple percentage)
    progress.mastery_level = progress.correct_answers / progress.total_questions
    progress.last_studied = datetime.utcnow()
    
    db.commit()
    db.refresh(db_response)
    return db_response

@router.get("/quiz/questions/{session_id}", response_model=List[QuizQuestionResponse])
async def get_session_questions(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all quiz questions for a session"""
    # Verify session belongs to user
    session = db.query(LearningSession).filter(
        LearningSession.id == session_id,
        LearningSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    questions = db.query(QuizQuestion).filter(
        QuizQuestion.session_id == session_id
    ).all()
    return questions