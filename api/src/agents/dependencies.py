from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class ChatDeps:
    db_session: AsyncSession
    session_id: str
    user_id: int
    temperature: float = 0.7
