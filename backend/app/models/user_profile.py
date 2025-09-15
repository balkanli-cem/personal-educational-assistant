from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    learning_style = Column(String(50), default="visual")
    difficulty_preference = Column(String(20), default="intermediate")
    subjects_of_interest = Column(JSON)  # Changed from ARRAY to JSON
    learning_goals = Column(Text)
    time_commitment = Column(String(20), default="medium")
    preferred_explanation_length = Column(String(20), default="medium")  # Added missing field
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="profile")