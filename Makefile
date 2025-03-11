PYTHON := python3
PIP := pip3
docker_compose := docker-compose

.PHONY: help install test run down clean

help:
	@echo "Available commands:"
	@echo "  make install    Install dependencies"
	@echo "  make test       Run tests with pytest"
	@echo "  make run        Run the service and MongoDB with Docker"
	@echo "  make down       Stop and remove running containers"
	@echo "  make clean      Remove all containers and volumes"

install:
	@echo "Installing dependencies..."
	@if ! command -v $(PYTHON) &> /dev/null; then \
		echo "Python3 is not installed. Please install it."; \
		exit 1; \
	fi
	@if ! command -v $(PIP) &> /dev/null; then \
		echo "pip3 is not installed. Please install it."; \
		exit 1; \
	fi
	@$(PIP) install -r requirements.txt

test:
	@echo "Running tests with pytest..."
	@$(PYTHON) -m pytest tests

run:
	@echo "Starting the service and MongoDB with Docker..."
	@$(docker_compose) up -d --build

down:
	@echo "Stopping all running services..."
	@$(docker_compose) down

clean:
	@echo "Removing all containers and volumes..."
	@$(docker_compose) down --rmi all --volumes --remove-orphans
