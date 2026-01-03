.PHONY: install dev test test-cov lint format run docker-up docker-down clean

# Install dependencies
install:
	uv venv
	uv pip install -r requirements.txt

# Install with dev dependencies
dev:
	uv venv
	uv pip install -r requirements.txt
	uv pip install -e ".[dev]"

# Run all tests
test:
	pytest tests/ -v

# Run tests with coverage
test-cov:
	pytest tests/ --cov=app --cov-report=term-missing --cov-report=html

# Run a single test file
test-file:
	pytest $(FILE) -v

# Lint code
lint:
	ruff check app/ tests/
	mypy app/

# Format code
format:
	black app/ tests/
	ruff check --fix app/ tests/

# Run the application locally
run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start Docker services
docker-up:
	docker-compose up -d

# Stop Docker services
docker-down:
	docker-compose down

# View Docker logs
docker-logs:
	docker-compose logs -f app

# Clean up
clean:
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# Help
help:
	@echo "Available commands:"
	@echo "  make install     - Create venv and install dependencies"
	@echo "  make dev         - Install with dev dependencies"
	@echo "  make test        - Run all tests"
	@echo "  make test-cov    - Run tests with coverage report"
	@echo "  make lint        - Run linters (ruff, mypy)"
	@echo "  make format      - Format code (black, ruff)"
	@echo "  make run         - Run the app locally"
	@echo "  make docker-up   - Start Docker services"
	@echo "  make docker-down - Stop Docker services"
	@echo "  make clean       - Clean up generated files"
