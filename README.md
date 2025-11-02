# Build Club x Meta - Multi-App Monorepo

A monorepo containing three applications for building AI-powered chat experiences:
- **API**: Primary AI chat and authentication service (FastAPI + Ollama + PostgreSQL)
- **Tools**: Standalone utility tools API (FastAPI)
- **UI**: Chat interface (SvelteKit + Bun)

## Architecture Overview

```
build-club-x-meta/
├── api/                    # Primary AI chat + auth service
│   ├── main.py            # FastAPI application
│   ├── src/               # Source code (routers, services, database)
│   ├── Dockerfile         # Container definition
│   └── pyproject.toml     # Dependencies
├── tools/                  # Utility tools API
│   ├── main.py            # FastAPI application
│   ├── src/               # Tool modules (calculator, text utils)
│   ├── Dockerfile         # Container definition
│   └── pyproject.toml     # Dependencies
├── ui/                     # SvelteKit frontend
│   ├── src/               # Svelte components and routes
│   └── package.json       # Bun dependencies
├── compose.yml             # Docker Compose orchestration
└── Makefile                # Development commands
```

## Prerequisites

- **Python 3.13+** with uv package manager ([Installation Guide](https://docs.astral.sh/uv/getting-started/installation/))
- **Bun** for UI development ([Installation Guide](https://bun.sh/))
- **Docker and Docker Compose** for containerized deployment
- At least 8GB of RAM (16GB recommended)
- ~5GB of disk space for the Llama model

## Quick Start

### Option 1: Docker Compose (All Services)

Start all services (API, Tools, Ollama, PostgreSQL):

```bash
make start
```

This will:
1. Start Ollama service and pull Llama 3.2 model (~4.7GB)
2. Start PostgreSQL for session/user storage
3. Start API service on http://localhost:8081
4. Start Tools service on http://localhost:8082

**Note:** First run takes several minutes to download the Llama model.

### Option 2: Local Development

Run each service individually for development:

```bash
# Terminal 1: API service
make api-dev

# Terminal 2: Tools service
make tools-dev

# Terminal 3: UI service
make ui-dev
```

Note: For API service, you'll still need Ollama and PostgreSQL running. Start them with:
```bash
docker compose up ollama postgres -d
```

## Available Commands

### Global Commands

```bash
make start        # Start all services with Docker Compose
make logs         # Show logs for all services
make stop         # Stop all services
make destroy      # Remove all containers, volumes, and networks
make help         # Show all available commands
```

### API Commands

```bash
make api-dev      # Start API in development mode (local, port 8000)
make api-logs     # Show logs for API service
make api-shell    # Enter API container shell
make api-test     # Run API tests
```

### Tools Commands

```bash
make tools-dev    # Start tools service (local, port 8000)
make tools-logs   # Show logs for tools service
make tools-shell  # Enter tools container shell
make tools-test   # Run tools tests
```

### UI Commands

```bash
make ui-dev       # Start UI dev server with Bun
make ui-install   # Install UI dependencies
make ui-build     # Build UI for production
make ui-preview   # Preview production build
```

## Services

### API Service (port 8081)

Primary AI chat and authentication interface powered by Llama 3.2 via Ollama.

**Key Features:**
- User registration and authentication
- Session management with PostgreSQL
- Streaming and non-streaming chat endpoints
- AI-powered conversation with history

**Endpoints:**
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get session
- `POST /api/chat` - Chat with AI (non-streaming)
- `POST /api/chat/stream` - Chat with AI (streaming)
- `GET /api/health` - Health check

**Documentation:** http://localhost:8081/docs

See [api/README.md](api/README.md) for detailed documentation.

### Tools Service (port 8082)

Standalone utility tools exposed via REST API.

**Available Tools:**
- **Calculator**: Basic arithmetic operations
- **Text Utilities**: Uppercase, lowercase, reverse, character/word count

**Endpoints:**
- `POST /calculator/calculate` - Perform arithmetic
- `POST /text/uppercase` - Convert to uppercase
- `POST /text/lowercase` - Convert to lowercase
- `POST /text/reverse` - Reverse text
- `POST /text/count` - Count characters and words
- `GET /health` - Health check

**Documentation:** http://localhost:8082/docs

See [tools/README.md](tools/README.md) for detailed documentation.

### UI Service (SvelteKit + Bun)

Modern chat interface built with SvelteKit and Bun.

See [ui/README.md](ui/README.md) for detailed documentation.

## Example Usage

### API: Chat with AI

```bash
curl -X POST "http://localhost:8081/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the capital of France?",
    "temperature": 0.7
  }'
```

### API: Streaming Chat

```bash
curl -X POST "http://localhost:8081/api/chat/stream" \
  -H "Content-Type: application/json" \
  -N \
  -d '{"message": "Tell me a joke"}'
```

### Tools: Calculator

```bash
curl -X POST "http://localhost:8082/calculator/calculate" \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 5, "b": 3}'
```

Response:
```json
{"result": 8.0, "operation": "add"}
```

### Tools: Text Utilities

```bash
curl -X POST "http://localhost:8082/text/uppercase" \
  -H "Content-Type: application/json" \
  -d '{"text": "hello world"}'
```

Response:
```json
{"result": "HELLO WORLD", "operation": "uppercase"}
```

## Configuration

### Environment Variables

Configured in `compose.yml`:

**API Service:**
- `OLLAMA_HOST`: Ollama service URL (default: `http://ollama:11434`)
- `MODEL_NAME`: LLM model name (default: `llama3.2`)
- `DATABASE_URL`: PostgreSQL connection string

**PostgreSQL:**
- `POSTGRES_USER`: Database user (default: `llama_user`)
- `POSTGRES_PASSWORD`: Database password (default: `llama_pass`)
- `POSTGRES_DB`: Database name (default: `llama_db`)

### Using Different Models

Edit `compose.yml` to use a different Llama model:

```yaml
environment:
  - MODEL_NAME=llama3.1  # or llama3, llama3.1:70b, etc.
```

Available models:
- `llama3.2` (default, ~4.7GB)
- `llama3.1` (~4.7GB)
- `llama3.1:70b` (larger, better quality, ~40GB)

### GPU Support (Optional)

Uncomment the GPU section in `compose.yml` under the ollama service:

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```

## Development Workflow

### Setting Up a New Service

Each service is self-contained:

```bash
# API service
cd api
uv sync          # Install dependencies
uv run uvicorn main:app --reload

# Tools service
cd tools
uv sync          # Install dependencies
uv run uvicorn main:app --reload

# UI service
cd ui
bun install      # Install dependencies
bun run dev      # Start dev server
```

### Adding Dependencies

**Python services (api, tools):**
```bash
cd api  # or tools
uv add <package-name>
uv sync
```

**UI service:**
```bash
cd ui
bun add <package-name>
```

## Troubleshooting

### Ollama Connection Issues

Check if Ollama is running:
```bash
docker compose ps
make logs
```

### Model Download Issues

The model downloads automatically. If it fails:
```bash
make destroy
make start
```

### Out of Memory

- Use a smaller model (llama3.2 is smallest)
- Close other applications
- Increase Docker's memory limit in Docker Desktop settings

### Port Conflicts

Modify ports in `compose.yml` if 8081 or 8082 are in use:
```yaml
ports:
  - "8083:80"  # Change to any available port
```

### Database Connection Issues

Check PostgreSQL is healthy:
```bash
docker compose ps postgres
docker compose logs postgres
```

## Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SvelteKit Documentation](https://kit.svelte.dev/)
- [Bun Documentation](https://bun.sh/docs)
- [Llama 3 Model Card](https://www.llama.com/docs/model-cards-and-prompt-formats/llama3_2/)
- [uv Documentation](https://docs.astral.sh/uv/)

## License

This project is open source and available for educational purposes.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review service-specific READMEs in each directory
3. Check Ollama, FastAPI, or SvelteKit documentation
4. Open an issue in the repository
