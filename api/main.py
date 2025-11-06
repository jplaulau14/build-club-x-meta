from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.database.database import init_db
from src.routers import auth, chat, chats, persona


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Llama Chat API",
    description="Chat API powered by Llama 3 via Ollama",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
api_router.include_router(chat.router)
api_router.include_router(chats.router)
api_router.include_router(persona.router)

app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Llama Chat API!",
        "docs": "/docs",
        "chat_endpoint": "/api/chat",
        "streaming_endpoint": "/api/chat/stream",
        "health_endpoint": "/api/health",
        "model": settings.model_name,
    }


@app.get("/reload-test")
async def reload_test():
    return {"status": "hot reload is working!", "version": 1}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
