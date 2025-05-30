#### Makefile ####
# This Makefile provides a set of convenient commands for managing a Dockerized
# Django project.

# Define variables for Docker Compose files
DOCKER_COMPOSE_DEV := docker-compose.dev.yml
DOCKER_COMPOSE_PROD := docker-compose.prod.yml

# Default container name (used for run_server/logs if not overridden)
CONTAINER_NAME_DEV := django-backend-dev
CONTAINER_NAME_PROD := django-backend-prod

# --- Core Docker Commands (Development) ---

# build-dev: Builds the Docker image for the backend service (dev).
# --no-cache: Forces a fresh build without using cached layers (useful during development).
build-dev:
	@docker compose -f $(DOCKER_COMPOSE_DEV) build --no-cache backend

cached_build-dev:
	@docker compose -f $(DOCKER_COMPOSE_DEV) build backend

# up-dev: Starts the backend service container in detached mode for development.
up-dev:
	@docker compose -f $(DOCKER_COMPOSE_DEV) up backend -d

# down-dev: Stops and removes the backend service container for development.
down-dev:
	@docker compose -f $(DOCKER_COMPOSE_DEV) down backend

# run_server-dev: Starts the Django development server inside the running dev container.
run_server-dev:
	@docker exec -it $(CONTAINER_NAME_DEV) poetry run python manage.py runserver 0.0.0.0:8000

# logs-dev: Displays the logs for the development container.
logs-dev:
	@docker logs -f $(CONTAINER_NAME_DEV)

# --- Core Docker Commands (Production) ---

# build-prod: Builds the Docker image for the backend service (prod).
# For production, you might not use --no-cache often unless you are debugging the build.
build-prod:
	@docker compose -f $(DOCKER_COMPOSE_PROD) build backend

# up-prod: Starts the backend service container in detached mode for production.
up-prod:
	@docker compose -f $(DOCKER_COMPOSE_PROD) up backend -d

# down-prod: Stops and removes the backend service container for production.
down-prod:
	@docker compose -f $(DOCKER_COMPOSE_PROD) down backend

# logs-prod: Displays the logs for the production container.
logs-prod:
	@docker logs -f $(CONTAINER_NAME_PROD)

# --- Database Commands (Adapt for dev/prod if needed) ---

# migrate-dev: Runs Django migrations for development.
migrate-dev:
	@docker exec -it $(CONTAINER_NAME_DEV) poetry run python manage.py migrate

# createsuperuser-dev: Creates a Django superuser for development.
createsuperuser-dev:
	@docker exec -it $(CONTAINER_NAME_DEV) poetry run python manage.py createsuperuser

# Shell into the development container
shell-dev:
	@docker exec -it $(CONTAINER_NAME_DEV) /bin/bash

# --- General Docker Commands ---

# status: Lists all Docker containers (running and stopped).
status:
	@docker ps -a

# --- Local Development Command ---

# local-launch: Runs the Django development server locally (outside Docker).
# This assumes you have a local Python environment with Poetry set up.
# IMPORTANT: Ensure your local environment is configured for `config.settings.dev`
# for this command to work as expected.
local-launch:
	@poetry run python manage.py runserver 0.0.0.0:8000