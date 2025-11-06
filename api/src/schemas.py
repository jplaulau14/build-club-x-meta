from datetime import datetime

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6)


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    session_id: str
    user_id: int
    username: str


class SessionResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime


class ChatSessionResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime


class MessageResponse(BaseModel):
    role: str
    content: str
    created_at: datetime
