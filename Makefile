.PHONY: help build up down logs clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build the Docker containers
	docker-compose build

up: ## Start the application
	docker-compose up -d

down: ## Stop the application
	docker-compose down

logs: ## View application logs
	docker-compose logs -f

clean: ## Clean up Docker containers and images
	docker-compose down -v
	docker system prune -f

dev: ## Start in development mode (with logs)
	docker-compose up --build

restart: ## Restart the application
	docker-compose restart

status: ## Check container status
	docker-compose ps 