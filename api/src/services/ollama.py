import json
from typing import AsyncGenerator

import httpx

from ..config import settings
from ..schemas import ChatRequest


class OllamaService:
    def __init__(self):
        self.host = settings.ollama_host
        self.model = settings.model_name

    async def health_check(self) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.host}/api/tags")
            response.raise_for_status()
            return response.json()

    async def chat(self, request: ChatRequest) -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": request.system_prompt},
                    {"role": "user", "content": request.message},
                ],
                "stream": False,
                "options": {"temperature": request.temperature},
            }

            response = await client.post(f"{self.host}/api/chat", json=payload)
            response.raise_for_status()

            result = response.json()
            return result.get("message", {}).get("content", "")

    async def chat_with_history(
        self, messages: list[dict], temperature: float = 0.7
    ) -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": temperature},
            }

            response = await client.post(f"{self.host}/api/chat", json=payload)
            response.raise_for_status()

            result = response.json()
            return result.get("message", {}).get("content", "")

    async def chat_stream(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        async with httpx.AsyncClient(timeout=120.0) as client:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": request.system_prompt},
                    {"role": "user", "content": request.message},
                ],
                "stream": True,
                "options": {"temperature": request.temperature},
            }

            async with client.stream(
                "POST", f"{self.host}/api/chat", json=payload
            ) as response:
                response.raise_for_status()

                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            chunk = json.loads(line)
                            if "message" in chunk:
                                content = chunk["message"].get("content", "")
                                if content:
                                    yield json.dumps({"content": content})

                            if chunk.get("done", False):
                                yield json.dumps({"done": True})
                        except json.JSONDecodeError:
                            continue

    async def chat_stream_with_history(
        self, messages: list[dict], temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        async with httpx.AsyncClient(timeout=120.0) as client:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": True,
                "options": {"temperature": temperature},
            }

            async with client.stream(
                "POST", f"{self.host}/api/chat", json=payload
            ) as response:
                response.raise_for_status()

                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            chunk = json.loads(line)
                            if "message" in chunk:
                                content = chunk["message"].get("content", "")
                                if content:
                                    yield json.dumps({"content": content})

                            if chunk.get("done", False):
                                yield json.dumps({"done": True})
                        except json.JSONDecodeError:
                            continue

    async def list_models(self) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.host}/api/tags")
            response.raise_for_status()
            return response.json()
