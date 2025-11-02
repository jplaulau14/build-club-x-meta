from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..database.database import get_db
from ..database.models import Session, User


async def get_current_user(
    x_session_id: Annotated[str, Header()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    result = await db.execute(
        select(Session).where(Session.id == x_session_id).options(selectinload(Session.user))
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")

    if session.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session expired")

    return session.user
