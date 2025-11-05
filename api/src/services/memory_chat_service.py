from pydantic_ai.messages import ModelMessage
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.chats import ChatManager
from ..database.message_adapter import MessageAdapter


async def get_message_history(chat_id: str, db: AsyncSession) -> list[ModelMessage]:
    manager = ChatManager(db)
    messages = await manager.get_chat_messages(chat_id)
    return MessageAdapter.db_to_pydantic(messages)
