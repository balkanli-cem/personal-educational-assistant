from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class LearningSessionBase(BaseModel):
    topic: str
    session_type: str  # explanation, quiz, evaluation
    content: str
    user_input: Optional[str] = None

class LearningSessionCreate(LearningSessionBase):
    pass

class LearningSessionResponse(LearningSessionBase):
    id: int
    user_id: int
    ai_response: Optional[str] = None
    session_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuizQuestionBase(BaseModel):
    question_text: str
    options: List[str]
    correct_answer: int
    explanation: Optional[str] = None
    difficulty_level: str = "medium"

class QuizQuestionCreate(QuizQuestionBase):
    session_id: int

class QuizQuestionResponse(QuizQuestionBase):
    id: int
    session_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuizResponseBase(BaseModel):
    selected_answer: int
    time_taken: Optional[int] = None

class QuizResponseCreate(QuizResponseBase):
    question_id: int

class QuizResponseResponse(QuizResponseBase):
    id: int
    question_id: int
    user_id: int
    is_correct: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class LearningProgressResponse(BaseModel):
    id: int
    user_id: int
    topic: str
    mastery_level: float
    total_sessions: int
    correct_answers: int
    total_questions: int
    last_studied: datetime
    
    class Config:
        from_attributes = True