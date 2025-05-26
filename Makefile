# This Makefile provides a set of convenient commands for managing a Dockerized
# Django project.

# --- Core Docker Commands ---

# build: Builds the Docker image for the backend service.
# --no-cache: Forces a fresh build without using cached layers (useful during development).
build:
	@docker compose -f docker-compose.yml build --no-cache backend

# up: Starts the backend service container in detached mode.
# -d: Runs the container in the background.
up:
	@docker compose -f docker-compose.yml up backend -d

# down: Stops and removes the backend service container.
# This also removes default networks created by docker compose.
down:
	@docker compose -f docker-compose.yml down backend

# run_server: Starts the Django development server inside the running container.
# This is useful for running the server manually after the container is up,
# or for debugging startup issues.
# -it: Keeps stdin open, allowing interaction (like Ctrl+C to stop).
# ${CONTAINER_NAME}: The name of the running container.
# poetry run: Executes the command within the container's Poetry virtual environment.
# python manage.py runserver 0.0.0.0:8000: The standard Django development server command.
run_server:
	@docker exec -it ${CONTAINER_NAME} poetry run python manage.py runserver 0.0.0.0:8000

# status: Lists all Docker containers (running and stopped).
# -a: Shows all containers, not just running ones.
status:
	@docker ps -a

# logs: Displays the logs for the specified container.
# ${CONTAINER_NAME}: A variable that needs to be defined elsewhere or replaced with the actual container name.
logs:
	@docker logs ${CONTAINER_NAME}

# --- Local Development Command ---

# local-launch: Runs the Django development server locally (outside Docker).
# This assumes you have a local Python environment with Poetry set up.
# poetry run: Executes the command within the Poetry virtual environment.
# python manage.py runserver 0.0.0.0:8000: Starts the Django development server listening on all interfaces on port 8000.
local-launch:
	@poetry run python manage.py runserver 0.0.0.0:8000

# Note: You might want to add more targets for common Django management commands
# like `makemigrations`, `migrate`, `createsuperuser`, `test`, etc.,
# using `docker exec` to run them inside the container.

