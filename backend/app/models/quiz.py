from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("learning_sessions.id", ondelete="CASCADE"), nullable=False)
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # array of answer options
    correct_answer = Column(Integer, nullable=False)  # index of correct option
    explanation = Column(Text)
    difficulty_level = Column(String(20), default="medium")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("LearningSession", back_populates="quiz_questions")
    responses = relationship("QuizResponse", back_populates="question")

class QuizResponse(Base):
    __tablename__ = "quiz_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("quiz_questions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    selected_answer = Column(Integer, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    time_taken = Column(Integer)  # seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    question = relationship("QuizQuestion", back_populates="responses")
    user = relationship("User", back_populates="quiz_responses")