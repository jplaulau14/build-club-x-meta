from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.dependencies import get_current_user
from ..core.sessions import SessionManager
from ..database.database import get_db
from ..database.models import User
from ..schemas import (
    LoginRequest,
    LoginResponse,
    MessageResponse,
    RegisterRequest,
    SessionResponse,
)

router = APIRouter(tags=["auth"])


@router.post("/auth/register", status_code=201)
async def register(
    request: RegisterRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    manager = SessionManager(db)
    try:
        user = await manager.create_user(request.username, request.password)
        return {"user_id": user.id, "username": user.username}
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")


@router.post("/auth/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    manager = SessionManager(db)
    user = await manager.authenticate_user(request.username, request.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session = await manager.create_session(user.id)
    return LoginResponse(session_id=session.id, user_id=user.id, username=user.username)


@router.get("/sessions", response_model=list[SessionResponse])
async def list_sessions(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    manager = SessionManager(db)
    sessions = await manager.get_user_sessions(current_user.id)
    return [
        SessionResponse(id=s.id, created_at=s.created_at, updated_at=s.updated_at)
        for s in sessions
    ]


@router.post("/sessions", response_model=SessionResponse, status_code=201)
async def create_session(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    manager = SessionManager(db)
    session = await manager.create_session(current_user.id)
    return SessionResponse(
        id=session.id, created_at=session.created_at, updated_at=session.updated_at
    )


@router.delete("/sessions/{session_id}", status_code=204)
async def delete_session(
    session_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    manager = SessionManager(db)
    session = await manager.get_session(session_id)

    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Session not found")

    await manager.delete_session(session_id)


@router.get("/sessions/{session_id}/messages", response_model=list[MessageResponse])
async def get_session_messages(
    session_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    manager = SessionManager(db)
    session = await manager.get_session(session_id)

    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = await manager.get_session_messages(session_id)
    return [
        MessageResponse(role=m.role, content=m.content, created_at=m.created_at)
        for m in messages
    ]
