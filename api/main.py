from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.database import init_db
from src.routers import auth, chats


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Llama Chat API - Starter Kit",
    description="Authentication and chat management boilerplate for Llama 3.2 workshop",
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
api_router.include_router(chats.router)

app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Llama Chat API - Starter Kit!",
        "docs": "/docs",
        "endpoints": {
            "auth": {
                "register": "/api/auth/register",
                "login": "/api/auth/login",
            },
            "chats": {
                "create": "/api/chats",
                "list": "/api/chats",
                "delete": "/api/chats/{chat_id}",
                "messages": "/api/chats/{chat_id}/messages",
            },
        },
    }


@app.get("/reload-test")
async def reload_test():
    return {"status": "hot reload is working!", "version": 1}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
