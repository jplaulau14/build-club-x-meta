from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.routers import chat

app = FastAPI(
    title="Llama Chat API",
    description="Chat API powered by Llama 3 via Ollama",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Llama Chat API!",
        "docs": "/docs",
        "chat_endpoint": "/chat",
        "streaming_endpoint": "/chat/stream",
        "health_endpoint": "/health",
        "model": settings.model_name,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
