.PHONY: help start logs logs-app logs-ollama stop destroy

help:
	@echo "Available commands:"
	@echo "  make start        - Start the application using quick-start.sh"
	@echo "  make logs         - Show logs for all services"
	@echo "  make logs-app     - Show logs for FastAPI app"
	@echo "  make logs-ollama  - Show logs for Ollama service"
	@echo "  make stop         - Stop all services"
	@echo "  make destroy      - Stop and remove all containers, volumes, and networks"

start:
	chmod +x quick-start.sh
	./quick-start.sh

logs:
	docker compose logs -f

logs-app:
	docker compose logs -f fastapi

logs-ollama:
	docker compose logs -f ollama

stop:
	docker compose stop

destroy:
	docker compose down -v --remove-orphans
