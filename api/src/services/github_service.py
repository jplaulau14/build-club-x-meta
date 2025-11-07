import json
import logging
from typing import AsyncGenerator

from ..agents.github_agent import github_agent

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def github_chat_stream(
    message: str,
    temperature: float = 0.7,
) -> AsyncGenerator[str, None]:
    try:
        logger.info(f"🚀 Starting GitHub agent with message: {message[:100]}...")
        tools_used = []
        last_message_count = 0

        async with github_agent.run_stream(
            message,
            model_settings={"temperature": temperature},
        ) as result:

            text_stream = result.stream_text(delta=True)

            async for text_delta in text_stream:
                yield f"data: {json.dumps({'type': 'text', 'content': text_delta})}\n\n"

                all_messages = result.all_messages()
                current_message_count = len(all_messages)

                if current_message_count > last_message_count:
                    new_messages = all_messages[last_message_count:]
                    logger.info(f"📨 Processing {len(new_messages)} new messages")

                    for msg in new_messages:
                        logger.info(f"📩 Message type: {type(msg).__name__}")

                        if hasattr(msg, 'parts'):
                            for part in msg.parts:
                                part_type = type(part).__name__
                                logger.info(f"    └─ Part type: {part_type}")

                                if hasattr(part, 'tool_name') and hasattr(part, 'args'):
                                    tool_name = part.tool_name
                                    tool_args = part.args

                                    logger.info(f"🔧 TOOL CALL: {tool_name}")
                                    logger.info(f"   Args: {tool_args}")

                                    if tool_name not in tools_used:
                                        tools_used.append(tool_name)

                                    annotation = {
                                        "type": "annotation",
                                        "annotation_type": "tool_call",
                                        "tool": tool_name,
                                        "args": tool_args,
                                        "timestamp": "executing"
                                    }
                                    yield f"data: {json.dumps(annotation)}\n\n"

                                elif hasattr(part, 'content') and part_type == 'ToolReturnPart':
                                    tool_name = tools_used[-1] if tools_used else "unknown"
                                    result_data = part.content

                                    logger.info(f"✅ TOOL RESULT: {tool_name}")
                                    logger.info(f"   Result preview: {str(result_data)[:100]}...")

                                    result_preview = str(result_data)[:200] if result_data else "No result"

                                    annotation = {
                                        "type": "annotation",
                                        "annotation_type": "tool_result",
                                        "tool": tool_name,
                                        "result_preview": result_preview,
                                        "result": result_data if isinstance(result_data, (dict, list)) else None,
                                        "timestamp": "completed"
                                    }
                                    yield f"data: {json.dumps(annotation)}\n\n"

                    last_message_count = current_message_count

            all_messages = result.all_messages()
            if len(all_messages) > last_message_count:
                new_messages = all_messages[last_message_count:]
                logger.info(f"📨 Processing final {len(new_messages)} messages")

                for msg in new_messages:
                    if hasattr(msg, 'parts'):
                        for part in msg.parts:
                            part_type = type(part).__name__

                            if hasattr(part, 'tool_name') and hasattr(part, 'args'):
                                tool_name = part.tool_name
                                tool_args = part.args

                                if tool_name not in tools_used:
                                    tools_used.append(tool_name)

                                annotation = {
                                    "type": "annotation",
                                    "annotation_type": "tool_call",
                                    "tool": tool_name,
                                    "args": tool_args,
                                    "timestamp": "executing"
                                }
                                yield f"data: {json.dumps(annotation)}\n\n"

                            elif hasattr(part, 'content') and part_type == 'ToolReturnPart':
                                tool_name = tools_used[-1] if tools_used else "unknown"
                                result_data = part.content
                                result_preview = str(result_data)[:200] if result_data else "No result"

                                annotation = {
                                    "type": "annotation",
                                    "annotation_type": "tool_result",
                                    "tool": tool_name,
                                    "result_preview": result_preview,
                                    "result": result_data if isinstance(result_data, (dict, list)) else None,
                                    "timestamp": "completed"
                                }
                                yield f"data: {json.dumps(annotation)}\n\n"

            logger.info(f"✨ Completed! Tools used: {tools_used}")

            yield f"data: {json.dumps({'type': 'done', 'tools_used': tools_used})}\n\n"

    except Exception as e:
        logger.error(f"❌ Error in github_chat_stream: {str(e)}", exc_info=True)
        error_event = {
            "type": "error",
            "message": str(e)
        }
        yield f"data: {json.dumps(error_event)}\n\n"
