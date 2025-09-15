from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.sql import func
from app.models.database import Base

class LearningSession(Base):
    __tablename__ = "learning_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    topic = Column(String(200), nullable=False)
    difficulty_level = Column(String(20), default="intermediate")
    learning_style = Column(String(50), default="visual")
    content = Column(Text)
    questions = Column(JSON)  # Changed from ARRAY(Text) to JSON
    answers = Column(JSON)   # Changed from ARRAY(Text) to JSON
    score = Column(Float)
    completed = Column(String(10), default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())