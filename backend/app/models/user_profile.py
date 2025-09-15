from sqlalchemy import Column, Integer, String, DateTime, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    learning_style = Column(String(50))  # visual, auditory, kinesthetic, reading
    difficulty_level = Column(String(20), default="beginner")  # beginner, intermediate, advanced
    subjects_of_interest = Column(ARRAY(String))  # array of subjects
    preferred_explanation_length = Column(String(20), default="medium")  # short, medium, detailed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="profile")