from datetime import datetime

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str
    system_prompt: str = "You are a helpful assistant."
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    response: str
    model: str


class PersonaRequest(BaseModel):
    message: str
    persona_name: str | None = None
    custom_system_prompt: str | None = None
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class PersonaResponse(BaseModel):
    response: str
    model: str
    persona_used: str


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
