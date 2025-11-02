FROM python:3.13-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# Set environment variables to suppress warnings
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

# Run the application with hot reload.
# Only watch src/ and main.py to avoid .venv changes triggering reload
CMD ["uv", "run", "uvicorn", "main:app", "--reload", "--reload-dir", "/app/src", "--reload-include", "main.py", "--port", "80", "--host", "0.0.0.0"]
