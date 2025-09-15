from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class LearningSession(Base):
    __tablename__ = "learning_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic = Column(String(200), nullable=False)
    session_type = Column(String(50), nullable=False)  # explanation, quiz, evaluation
    content = Column(Text, nullable=False)
    user_input = Column(Text)
    ai_response = Column(Text)
    session_data = Column(JSON)  # flexible data storage
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="learning_sessions")
    quiz_questions = relationship("QuizQuestion", back_populates="session")