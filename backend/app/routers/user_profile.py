from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..models.database import get_db
from ..models.user import User
from ..models.user_profile import UserProfile
from ..models.learning_progress import LearningProgress
from ..schemas.user import UserProfileCreate, UserProfileResponse
from ..schemas.educational import LearningProgressResponse
from .auth import get_current_user

router = APIRouter()

@router.get("/", response_model=UserProfileResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    return profile

@router.put("/", response_model=UserProfileResponse)
async def update_user_profile(
    profile_data: UserProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    
    # Update profile fields
    for field, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/progress", response_model=List[LearningProgressResponse])
async def get_learning_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's learning progress"""
    progress = db.query(LearningProgress).filter(
        LearningProgress.user_id == current_user.id
    ).all()
    return progress

@router.get("/progress/{topic}", response_model=LearningProgressResponse)
async def get_topic_progress(
    topic: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get learning progress for a specific topic"""
    progress = db.query(LearningProgress).filter(
        LearningProgress.user_id == current_user.id,
        LearningProgress.topic == topic
    ).first()
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No progress found for this topic"
        )
    return progress