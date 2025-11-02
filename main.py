import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx
from typing import Optional, AsyncGenerator

app = FastAPI(
    title="Llama Chat API",
    description="Simple chat API powered by Llama 3 via Ollama",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2")


class ChatRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = "You are a helpful assistant."
    temperature: Optional[float] = 0.7


class ChatResponse(BaseModel):
    response: str
    model: str


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Llama Chat API!",
        "docs": "/docs",
        "chat_endpoint": "/chat",
        "streaming_endpoint": "/chat/stream",
        "health_endpoint": "/health",
        "model": MODEL_NAME
    }


@app.get("/health")
async def health_check():
    """Health check endpoint to verify Ollama connectivity."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{OLLAMA_HOST}/api/tags")
            response.raise_for_status()
            return {
                "status": "healthy",
                "ollama_host": OLLAMA_HOST,
                "model": MODEL_NAME,
                "available_models": response.json()
            }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Ollama service unavailable: {str(e)}"
        )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint to interact with Llama 3.

    - **message**: The user's message
    - **system_prompt**: Optional system prompt to set context
    - **temperature**: Optional temperature for response randomness (0.0 to 1.0)
    """
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": request.system_prompt},
                    {"role": "user", "content": request.message}
                ],
                "stream": False,
                "options": {
                    "temperature": request.temperature
                }
            }

            response = await client.post(
                f"{OLLAMA_HOST}/api/chat",
                json=payload
            )
            response.raise_for_status()

            result = response.json()
            assistant_message = result.get("message", {}).get("content", "")

            return ChatResponse(
                response=assistant_message,
                model=MODEL_NAME
            )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Request to Ollama timed out"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Ollama API error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint to interact with Llama 3.
    Returns Server-Sent Events (SSE) with real-time token generation.

    - **message**: The user's message
    - **system_prompt**: Optional system prompt to set context
    - **temperature**: Optional temperature for response randomness (0.0 to 1.0)
    """
    async def generate() -> AsyncGenerator[str, None]:
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                payload = {
                    "model": MODEL_NAME,
                    "messages": [
                        {"role": "system", "content": request.system_prompt},
                        {"role": "user", "content": request.message}
                    ],
                    "stream": True,
                    "options": {
                        "temperature": request.temperature
                    }
                }

                async with client.stream(
                    "POST",
                    f"{OLLAMA_HOST}/api/chat",
                    json=payload
                ) as response:
                    response.raise_for_status()

                    async for line in response.aiter_lines():
                        if line.strip():
                            try:
                                chunk = json.loads(line)
                                if "message" in chunk:
                                    content = chunk["message"].get("content", "")
                                    if content:
                                        # Send as Server-Sent Event
                                        yield f"data: {json.dumps({'content': content})}\n\n"

                                # Check if this is the final chunk
                                if chunk.get("done", False):
                                    yield f"data: {json.dumps({'done': True})}\n\n"
                            except json.JSONDecodeError:
                                continue

        except httpx.TimeoutException:
            error_msg = json.dumps({"error": "Request to Ollama timed out"})
            yield f"data: {error_msg}\n\n"
        except httpx.HTTPStatusError as e:
            error_msg = json.dumps({"error": f"Ollama API error: {str(e)}"})
            yield f"data: {error_msg}\n\n"
        except Exception as e:
            error_msg = json.dumps({"error": f"Internal server error: {str(e)}"})
            yield f"data: {error_msg}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.get("/models")
async def list_models():
    """List all available models in Ollama."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{OLLAMA_HOST}/api/tags")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to fetch models: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
