# Llama-Powered Chat Application Workshop

A workshop boilerplate to build your own Llama-powered application using Meta's Llama 3, Ollama, and FastAPI.

## What You'll Build

A complete chat API powered by Llama 3.2 that includes:
- FastAPI-based REST API
- Chat endpoint for complete responses
- Streaming endpoint for real-time token generation (SSE)
- Docker Compose setup for easy deployment
- Automatic model downloading and setup
- Web-based chat interface

## Prerequisites

- uv package manager ([Installation Guide](https://docs.astral.sh/uv/getting-started/installation/))
- Docker and Docker Compose installed
- At least 8GB of RAM (16GB recommended)
- ~5GB of disk space for the Llama model

## Quick Start

### 1. Clone and Navigate

```bash
git clone <your-repo-url>
cd build-club-x-meta
```

### 2. Start Everything with Make (Recommended)

```bash
make start
```

Or manually:
```bash
chmod +x quick-start.sh
./quick-start.sh
```

This will:
1. Check that Docker is installed and running
2. Start the Ollama service
3. Automatically pull the Llama 3.2 model (~4.7GB)
4. Start the FastAPI application
5. Wait for services to be ready
6. Make the API available at `http://localhost:8081`

**Note:** The first run will take several minutes to download the Llama model.

### Useful Make Commands

```bash
make start        # Start the application
make logs         # View all service logs
make logs-app     # View FastAPI app logs only
make logs-ollama  # View Ollama service logs only
make stop         # Stop all services
make destroy      # Remove all containers, volumes, and networks
make help         # Show all available commands
```

### 3. Verify Everything is Running

Open your browser and go to:
- API Documentation: http://localhost:8081/docs
- Health Check: http://localhost:8081/api/health

## Using the API

### Interactive Documentation

Visit http://localhost:8081/docs for an interactive Swagger UI where you can test all endpoints.

### Example: Chat Endpoint

**Request:**
```bash
curl -X POST "http://localhost:8081/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the capital of France?",
    "system_prompt": "You are a helpful assistant.",
    "temperature": 0.7
  }'
```

**Response:**
```json
{
  "response": "The capital of France is Paris.",
  "model": "llama3.2"
}
```

### Example: Using Python

```python
import requests

response = requests.post(
    "http://localhost:8081/api/chat",
    json={
        "message": "Explain quantum computing in simple terms",
        "temperature": 0.7
    }
)

print(response.json()["response"])
```

### Example: Using JavaScript

```javascript
fetch('http://localhost:8081/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Write a haiku about coding',
    temperature: 0.9
  })
})
.then(response => response.json())
.then(data => console.log(data.response));
```

### Example: Streaming Chat (Real-time Response)

The `/api/chat/stream` endpoint provides real-time streaming responses using Server-Sent Events (SSE).

**Using Python:**
```python
import requests
import json

url = "http://localhost:8081/api/chat/stream"
payload = {
    "message": "Write a short story about a robot",
    "temperature": 0.8
}

with requests.post(url, json=payload, stream=True) as response:
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data = json.loads(line[6:])
                if 'content' in data:
                    print(data['content'], end='', flush=True)
                elif 'done' in data:
                    print()
                    break
```

**Using JavaScript (EventSource):**
```javascript
const message = encodeURIComponent(JSON.stringify({
  message: "Explain machine learning",
  temperature: 0.7
}));

const eventSource = new EventSource(
  `http://localhost:8081/api/chat/stream?message=${message}`
);

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.content) {
    console.log(data.content);
  }
  if (data.done) {
    eventSource.close();
  }
};
```

**Using curl:**
```bash
curl -X POST "http://localhost:8081/api/chat/stream" \
  -H "Content-Type: application/json" \
  -N \
  -d '{"message": "Tell me a joke"}'
```

### Web Interface

A ready-to-use chat interface is included! Simply open `chat.html` in your browser:

```bash
open chat.html    # macOS
xdg-open chat.html    # Linux
start chat.html   # Windows
```

Or just double-click the file.

**Features:**
- Real-time streaming chat interface
- Toggle between streaming and non-streaming modes
- Adjustable temperature control
- Clean, modern UI with message history
- Auto-scrolling and typing indicators
- Keyboard shortcuts (Enter to send, Shift+Enter for new line)

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and available endpoints |
| `/api/health` | GET | Health check and Ollama connectivity status |
| `/api/chat` | POST | Send a message and get a complete response from Llama |
| `/api/chat/stream` | POST | Send a message and get a streaming response (SSE) |
| `/api/models` | GET | List all available models in Ollama |
| `/docs` | GET | Interactive API documentation (Swagger UI) |

## Configuration

### Environment Variables

You can customize the setup by modifying the `compose.yml` file:

- `OLLAMA_HOST`: Ollama service URL (default: `http://ollama:11434`)
- `MODEL_NAME`: Llama model to use (default: `llama3.2`)

### Using Different Models

To use a different Llama model, edit `compose.yml`:

```yaml
environment:
  - MODEL_NAME=llama3.1  # or llama3, llama3.1:70b, etc.
```

Available models:
- `llama3.2` (default, ~4.7GB)
- `llama3.1` (~4.7GB)
- `llama3.1:70b` (larger, better quality, ~40GB)

### GPU Support (Optional)

If you have an NVIDIA GPU, uncomment the GPU section in `compose.yml`:

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```

## Local Development (Without Docker)

### 1. Install Ollama

Download and install from https://ollama.ai

### 2. Pull the Model

```bash
ollama pull llama3.2
```

### 3. Install Python Dependencies

```bash
uv venv
uv sync
source .venv/bin/activate
```

### 4. Run the API

```bash
uvicorn main:app --reload

# or run with uv
uv run uvicorn main:app --reload
```

The API will be available at http://localhost:8081

## Project Structure

```
build-club-x-meta/
├── compose.yml                  # Docker Compose configuration
├── Dockerfile                   # FastAPI container definition
├── Makefile                     # Make commands for common tasks
├── main.py                      # FastAPI application entry point
├── requirements.txt             # Python dependencies
├── pyproject.toml               # Project metadata
├── chat.html                    # Web-based chat interface
├── quick-start.sh               # Quick start script
├── src/                         # Application source code
│   ├── config.py               # Configuration management
│   ├── schemas.py              # Pydantic models
│   ├── routers/                # API routers
│   │   └── chat.py            # Chat endpoints
│   └── services/               # Business logic
│       └── ollama.py          # Ollama service
└── README.md                    # This file
```

## Troubleshooting

### Ollama Connection Issues

Check if Ollama is running:
```bash
docker compose ps
```

View Ollama logs:
```bash
make logs-ollama
# or
docker compose logs ollama
```

### Model Download Issues

The model download happens automatically. If it fails:
```bash
docker compose down -v
docker compose up --build
```

### Out of Memory

If you encounter memory issues, try:
1. Using a smaller model (llama3.2 is the smallest)
2. Closing other applications
3. Increasing Docker's memory limit in Docker Desktop settings

### Port Conflicts

If port 8081 or 11434 is already in use, modify the ports in `compose.yml`:
```yaml
ports:
  - "8082:8000"  # Change 8082 to any available port
```

## Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Llama 3 Model Card](https://www.llama.com/docs/model-cards-and-prompt-formats/llama3_2/)

## License

This project is open source and available for educational purposes.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Ollama and FastAPI documentation
3. Open an issue in the repository
