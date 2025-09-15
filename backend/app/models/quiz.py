from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    topic = Column(String(200), nullable=False)
    difficulty_level = Column(String(20), default="intermediate")
    questions = Column(JSON)
    correct_answers = Column(JSON)
    user_answers = Column(JSON)
    score = Column(Float)
    completed = Column(String(10), default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("learning_sessions.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    options = Column(JSON)  # Changed from ARRAY to JSON
    correct_answer = Column(String(10), nullable=False)
    explanation = Column(Text)
    difficulty_level = Column(String(20), default="easy")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("LearningSession", back_populates="quiz_questions")
    responses = relationship("QuizResponse", back_populates="question")

class QuizResponse(Base):
    __tablename__ = "quiz_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    selected_answer = Column(String(10), nullable=False)
    is_correct = Column(String(10), default="false")
    time_taken = Column(Integer)  # in seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    question = relationship("QuizQuestion", back_populates="responses")
    user = relationship("User", back_populates="quiz_responses")