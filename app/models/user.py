from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr = Field(example="test@example.com")
    full_name: str = Field(example="Test User")

class UserCreate(UserBase):
    password: str = Field(example="testpassword")

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, example="test@example.com")
    full_name: Optional[str] = Field(None, example="Test User")
    password: Optional[str] = Field(None, example="newpassword")

class UserInDB(UserBase):
    id: int = Field(example=1)
    hashed_password: str
    created_at: datetime = Field(example="2024-03-23T12:00:00")
    updated_at: Optional[datetime] = Field(None, example="2024-03-23T12:00:00")

    class Config:
        from_attributes = True

class User(UserBase):
    id: int = Field(example=1)
    created_at: datetime = Field(example="2024-03-23T12:00:00")
    updated_at: Optional[datetime] = Field(None, example="2024-03-23T12:00:00")

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str = Field(example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(example="bearer")

class TokenData(BaseModel):
    email: Optional[str] = Field(None, example="test@example.com") 