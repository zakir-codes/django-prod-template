# Use a slim Python base image for smaller size
FROM python:3.12-slim

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_ANSI=1

# Install system dependencies
# Combine apt-get commands to reduce layers
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
    # Clean up apt cache to keep image size down
    && rm -rf /var/lib/apt/lists/*

# Install Poetry globally
# Using pip to install poetry before copying project files
RUN pip install poetry

# Set the working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock first to leverage Docker cache
# This ensures that if only application code changes, dependencies aren't reinstalled
COPY pyproject.toml poetry.lock ./

# Install project dependencies
# Poetry will install dependencies directly into the system's site-packages
# thanks to POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-root

# Copy the rest of the application code
# This step comes after dependency installation
COPY . .

# Collect static files
# Now that all dependencies are installed and the project is copied,
# Django and manage.py should be fully accessible.
# RUN python manage.py collectstatic --noinput

# Expose the port Gunicorn will listen on
EXPOSE 8000

# Command to run the application using Gunicorn
# Using "exec" form for CMD for better signal handling
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--log-file", "-"]