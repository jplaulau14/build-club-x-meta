"""
GitHub Chat Router - Demonstrates Tool Calling with PydanticAI

This router provides endpoints for the GitHub agent workshop,
demonstrating progressive tool calling complexity across 4 stages.

Endpoints:
    POST /api/github/chat - Streaming chat with GitHub agent and tools
"""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ..schemas import ChatRequest
from ..services import github_service

router = APIRouter(prefix="/github", tags=["github"])


# ============================================================================
# STAGES 1-3: Basic Streaming Endpoint
# ============================================================================

@router.post("/chat")
async def github_chat(request: ChatRequest):
    """
    Chat with GitHub agent using tool calling.

    This endpoint demonstrates:
    - Stage 1: Single tool (search_repositories)
    - Stage 2: Multiple tools with intelligent selection
    - Stage 3: Tool chaining for complex queries

    The agent has access to GitHub API tools and will automatically
    decide when and how to use them based on the user's question.

    Request body:
        - message (str): User's question or request
        - temperature (float, optional): Model temperature 0.0-2.0 (default: 0.7)

    Response:
        Server-Sent Events stream with JSON data:
        - {"content": "text"} - Streaming response text
        - {"done": true} - End of stream signal

    Example queries:
        - "Find popular React libraries"
        - "Tell me about facebook/react"
        - "Find Python web frameworks and show me issues for the top one"
    """
    return StreamingResponse(
        github_service.github_chat_stream(
            message=request.message,
            temperature=request.temperature
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        },
    )


# ============================================================================
# STAGE 4: Enhanced Streaming with Tool Visibility
# ============================================================================
# For workshop: Uncomment this endpoint and update the frontend to use it
# This provides real-time visibility into tool execution

"""
@router.post("/chat/enhanced")
async def github_chat_enhanced(request: ChatRequest):
    '''
    Chat with GitHub agent with tool call visualization.

    This enhanced endpoint (Stage 4) provides real-time visibility into:
    - Which tools are being called
    - Tool arguments
    - Tool results
    - Final agent response

    Response event types:
        - {"type": "tool_call", "tool": "name", "args": {...}}
        - {"type": "tool_result", "tool": "name", "result": {...}}
        - {"type": "text", "content": "partial text"}
        - {"type": "done", "tools_used": ["tool1", "tool2"]}
        - {"type": "error", "message": "error description"}

    This allows the frontend to show:
    - "🔧 Calling search_repositories..."
    - "✅ Found 5 repositories"
    - Live progress through multi-step queries
    '''
    return StreamingResponse(
        github_service.github_chat_stream_with_tools(
            message=request.message,
            temperature=request.temperature
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
"""


# ============================================================================
# Alternative Stage 4 Endpoint (Simpler Implementation)
# ============================================================================

"""
@router.post("/chat/tools")
async def github_chat_tools(request: ChatRequest):
    '''
    Chat with GitHub agent showing tool usage summary.

    A simpler Stage 4 alternative that shows which tools were used
    without real-time tracking of each individual tool call.

    Response includes:
        - {"type": "text", "content": "..."} - Streaming text
        - {"type": "done", "tools_used": ["tool1", "tool2"]} - Summary
    '''
    return StreamingResponse(
        github_service.github_chat_stream_enhanced(
            message=request.message,
            temperature=request.temperature
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
"""
