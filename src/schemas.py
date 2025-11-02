from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str
    system_prompt: str = "You are a helpful assistant."
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    response: str
    model: str
