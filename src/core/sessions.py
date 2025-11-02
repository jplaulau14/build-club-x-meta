from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Message, Session, User
from .auth import hash_password, verify_password


class SessionManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, username: str, password: str) -> User:
        password_hash = hash_password(password)
        user = User(username=username, password_hash=password_hash)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if user and verify_password(password, user.password_hash):
            return user
        return None

    async def create_session(self, user_id: int) -> Session:
        session = Session(
            id=str(uuid4()),
            user_id=user_id,
            expires_at=datetime.utcnow() + timedelta(hours=24),
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def get_session(self, session_id: str) -> Optional[Session]:
        result = await self.db.execute(select(Session).where(Session.id == session_id))
        return result.scalar_one_or_none()

    async def delete_session(self, session_id: str) -> bool:
        session = await self.get_session(session_id)
        if session:
            await self.db.delete(session)
            await self.db.commit()
            return True
        return False

    async def add_message(self, session_id: str, role: str, content: str) -> Message:
        message = Message(session_id=session_id, role=role, content=content)
        self.db.add(message)

        session = await self.get_session(session_id)
        if session:
            session.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_session_messages(self, session_id: str) -> list[Message]:
        result = await self.db.execute(
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.created_at)
        )
        return list(result.scalars().all())

    async def get_user_sessions(self, user_id: int) -> list[Session]:
        result = await self.db.execute(
            select(Session)
            .where(Session.user_id == user_id)
            .order_by(Session.updated_at.desc())
        )
        return list(result.scalars().all())
