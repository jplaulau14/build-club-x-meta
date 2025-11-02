.PHONY: help start logs stop destroy api-dev api-logs api-shell api-test tools-dev tools-logs tools-shell tools-test ui-dev ui-install ui-build ui-preview

help:
	@echo "Available commands:"
	@echo ""
	@echo "Global commands:"
	@echo "  make start        - Start all services with Docker Compose"
	@echo "  make logs         - Show logs for all services"
	@echo "  make stop         - Stop all services"
	@echo "  make destroy      - Stop and remove all containers, volumes, and networks"
	@echo ""
	@echo "API commands:"
	@echo "  make api-dev      - Start API in development mode (local)"
	@echo "  make api-logs     - Show logs for API service"
	@echo "  make api-shell    - Enter API container shell"
	@echo "  make api-test     - Run API tests"
	@echo ""
	@echo "Tools commands:"
	@echo "  make tools-dev    - Start tools service in development mode (local)"
	@echo "  make tools-logs   - Show logs for tools service"
	@echo "  make tools-shell  - Enter tools container shell"
	@echo "  make tools-test   - Run tools tests"
	@echo ""
	@echo "UI commands:"
	@echo "  make ui-dev       - Start UI dev server with Bun"
	@echo "  make ui-install   - Install UI dependencies"
	@echo "  make ui-build     - Build UI for production"
	@echo "  make ui-preview   - Preview production build"

# Global commands
start:
	chmod +x quick-start.sh
	./quick-start.sh

logs:
	docker compose logs -f

stop:
	docker compose stop

destroy:
	docker compose down -v --remove-orphans

# API commands
api-dev:
	cd api && uv run uvicorn main:app --reload --port 8000

api-logs:
	docker compose logs -f api

api-shell:
	docker compose exec api /bin/sh

api-test:
	cd api && uv run pytest

# Tools commands
tools-dev:
	cd tools && uv run uvicorn main:app --reload --port 8000

tools-logs:
	docker compose logs -f tools

tools-shell:
	docker compose exec tools /bin/sh

tools-test:
	cd tools && uv run pytest

# UI commands
ui-dev:
	cd ui && bun run dev

ui-install:
	cd ui && bun install

ui-build:
	cd ui && bun run build

ui-preview:
	cd ui && bun run preview
