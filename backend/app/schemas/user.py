from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserProfileBase(BaseModel):
    learning_style: Optional[str] = None
    difficulty_level: str = "beginner"
    subjects_of_interest: Optional[List[str]] = None
    preferred_explanation_length: str = "medium"

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileResponse(UserProfileBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True