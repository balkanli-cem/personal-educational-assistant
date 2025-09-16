from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel

from ..models.database import get_db
from ..models.user import User
from ..models.user_profile import UserProfile
from ..models.learning_session import LearningSession
from ..models.quiz import QuizQuestion, QuizResponse
#from ..services.llm_service import llm_service
from ..services.openai_service import openai_service as llm_service
from .auth import get_current_user

router = APIRouter()

class ExplanationRequest(BaseModel):
    topic: str
    user_input: str

class QuizRequest(BaseModel):
    topic: str
    difficulty_level: str = "beginner"
    num_questions: int = 5

class LearningPathRequest(BaseModel):
    topic: str
    current_level: str = "beginner"
    learning_goals: List[str] = []

@router.post("/explain")
async def get_explanation(
    request: ExplanationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-generated explanation for a topic"""
    try:
        # Get user profile for personalization
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        # Get user's learning history for better personalization
        recent_sessions = db.query(LearningSession).filter(
            LearningSession.user_id == current_user.id,
            LearningSession.session_type == "explanation"
        ).order_by(LearningSession.created_at.desc()).limit(5).all()
        
        # Get user's quiz performance (simplified)
        recent_quizzes = db.query(QuizResponse).filter(
            QuizResponse.user_id == current_user.id
        ).limit(5).all()
        
        # Calculate performance level for better personalization
        if recent_quizzes:
            correct_answers = sum(1 for q in recent_quizzes if q.is_correct)
            total_answers = len(recent_quizzes)
            performance_level = "advanced" if (correct_answers / total_answers) > 0.8 else "intermediate" if (correct_answers / total_answers) > 0.6 else "beginner"
        else:
            performance_level = profile.difficulty_level or "beginner"
        
        # Generate explanation with enhanced personalization
        explanation = await llm_service.generate_explanation(
            topic=request.topic,
            user_input=request.user_input,
            learning_style=profile.learning_style or "visual",
            difficulty_level=performance_level,  # Use calculated performance level
            explanation_length=profile.preferred_explanation_length or "medium"
        )
        
        # Save to learning session
        session = LearningSession(
            user_id=current_user.id,
            topic=request.topic,
            session_type="explanation",
            content=explanation,
            user_input=request.user_input,
            ai_response=explanation
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return {
            "explanation": explanation,
            "session_id": session.id,
            "personalized_for": {
                "learning_style": profile.learning_style,
                "difficulty_level": performance_level,
                "performance_based": True
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating explanation: {str(e)}"
        )

@router.post("/quiz/generate")
async def generate_quiz(
    request: QuizRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate AI-powered quiz for a topic"""
    try:
        # Input validation
        if not request.topic.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Topic cannot be empty"
            )
        
        if request.num_questions < 1 or request.num_questions > 20:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Number of questions must be between 1 and 20"
            )
        
        if request.difficulty_level not in ["beginner", "intermediate", "advanced"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Difficulty level must be beginner, intermediate, or advanced"
            )
        
        # Generate quiz questions
        questions = await llm_service.generate_quiz(
            topic=request.topic,
            difficulty_level=request.difficulty_level,
            num_questions=request.num_questions
            )
        
        if "error" in questions[0] if questions else True:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=questions[0]["error"] if questions else "Error generating quiz"
            )
        
        # Create learning session
        session = LearningSession(
            user_id=current_user.id,
            topic=request.topic,
            session_type="quiz",
            content=f"Generated {len(questions)} quiz questions",
            session_data={"difficulty_level": request.difficulty_level}
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        # Save questions to database
        saved_questions = []
        for q in questions:
            question = QuizQuestion(
                session_id=session.id,
                question_text=q["question"],
                options=q["options"],
                correct_answer=q["correct_answer"],
                explanation=q.get("explanation", ""),
                difficulty_level=request.difficulty_level
            )
            db.add(question)
            db.commit()
            db.refresh(question)
            saved_questions.append(question)
        
        return {
            "session_id": session.id,
            "topic": request.topic,
            "difficulty_level": request.difficulty_level,
            "questions": [
                {
                    "id": q.id,
                    "question": q.question_text,
                    "options": q.options,
                    "correct_answer": q.correct_answer,
                    "explanation": q.explanation
                }
                for q in saved_questions
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating quiz: {str(e)}"
        )

@router.post("/learning-path")
async def generate_learning_path(
    request: LearningPathRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate personalized learning path"""
    try:
        learning_path = await llm_service.generate_learning_path(
            topic=request.topic,
            current_level=request.current_level,
            learning_goals=request.learning_goals
        )
        
        if "error" in learning_path:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=learning_path["error"]
            )
        
        return learning_path
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating learning path: {str(e)}"
        )

@router.post("/evaluate")
async def evaluate_answer(
    question_id: int,
    user_answer: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Evaluate user's answer and provide feedback"""
    try:
        # Get question
        question = db.query(QuizQuestion).filter(
            QuizQuestion.id == question_id
        ).first()
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found"
            )
        
        # Check if answer is correct
        is_correct = user_answer == question.correct_answer
        
        # Generate AI feedback
        feedback = await llm_service.evaluate_answer(
            topic=question.session.topic,
            question=question.question_text,
            correct_answer=str(question.correct_answer),
            user_response=user_answer
        )
        
        # Save response
        response = QuizResponse(
            question_id=question_id,
            user_id=current_user.id,
            selected_answer=user_answer,
            is_correct=is_correct
        )
        db.add(response)
        db.commit()
        db.refresh(response)
        
        return {
            "is_correct": is_correct,
            "feedback": feedback,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error evaluating answer: {str(e)}"
        )

class QuizSubmissionRequest(BaseModel):
    session_id: int
    answers: List[Dict[str, Any]]  # [{"question_id": int, "selected_answer": int}]

@router.post("/quiz/submit")
async def submit_quiz(
    request: QuizSubmissionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit quiz answers and get results"""
    try:
        # Get all questions for this session
        questions = db.query(QuizQuestion).filter(
            QuizQuestion.session_id == request.session_id
        ).all()
        
        if not questions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz session not found"
            )
        
        # Process answers
        results = []
        total_score = 0
        
        for answer in request.answers:
            question_id = answer["question_id"]
            selected_answer = answer["selected_answer"]
            
            # Find the question
            question = next((q for q in questions if q.id == question_id), None)
            if not question:
                continue
            
            # Check if answer is correct
            is_correct = selected_answer == question.correct_answer
            if is_correct:
                total_score += 1
            
            # Save response
            response = QuizResponse(
                question_id=question_id,
                user_id=current_user.id,
                selected_answer=selected_answer,
                is_correct=is_correct
            )
            db.add(response)
            
            results.append({
                "question_id": question_id,
                "question": question.question_text,
                "selected_answer": selected_answer,
                "correct_answer": question.correct_answer,
                "is_correct": is_correct,
                "explanation": question.explanation
            })
        
        db.commit()
        
        # Calculate percentage
        percentage = (total_score / len(questions)) * 100
        
        return {
            "total_questions": len(questions),
            "correct_answers": total_score,
            "percentage": round(percentage, 1),
            "results": results,
            "grade": get_grade(percentage)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error submitting quiz: {str(e)}"
        )

def get_grade(percentage: float) -> str:
    """Get letter grade based on percentage"""
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B+"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C+"
    else:
        return "C"