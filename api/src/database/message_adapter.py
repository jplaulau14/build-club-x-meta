from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    SystemPromptPart,
    TextPart,
    UserPromptPart,
)

from .models import Message


class MessageAdapter:
    @staticmethod
    def db_to_pydantic(messages: list[Message]) -> list[ModelMessage]:
        pydantic_messages = []

        for msg in messages:
            if msg.role == "user":
                pydantic_messages.append(
                    ModelRequest(parts=[UserPromptPart(content=msg.content)])
                )
            elif msg.role == "system":
                pydantic_messages.append(
                    ModelRequest(parts=[SystemPromptPart(content=msg.content)])
                )
            elif msg.role == "assistant":
                pydantic_messages.append(
                    ModelResponse(parts=[TextPart(content=msg.content)])
                )

        return pydantic_messages

    @staticmethod
    def pydantic_to_db_dict(messages: list[ModelMessage]) -> list[dict]:
        db_messages = []

        for msg in messages:
            if isinstance(msg, ModelRequest):
                for part in msg.parts:
                    if isinstance(part, UserPromptPart):
                        db_messages.append({"role": "user", "content": part.content})
                    elif isinstance(part, SystemPromptPart):
                        db_messages.append({"role": "system", "content": part.content})
            elif isinstance(msg, ModelResponse):
                content = msg.text
                if content:
                    db_messages.append({"role": "assistant", "content": content})

        return db_messages
