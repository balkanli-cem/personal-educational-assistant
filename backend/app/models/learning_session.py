from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class LearningSession(Base):
    __tablename__ = "learning_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    topic = Column(String(200), nullable=False)
    session_type = Column(String(50), default="explanation")  # Added missing field
    difficulty_level = Column(String(20), default="intermediate")
    learning_style = Column(String(50), default="visual")
    content = Column(Text)
    user_input = Column(Text)  # Added missing field
    ai_response = Column(Text)  # Added missing field
    session_data = Column(JSON)  # Added missing field
    questions = Column(JSON)
    answers = Column(JSON)
    score = Column(Float)
    completed = Column(String(10), default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="learning_sessions")
    quiz_questions = relationship("QuizQuestion", back_populates="session")