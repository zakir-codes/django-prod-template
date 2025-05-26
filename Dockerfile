# Production-ready Dockerfile using Poetry and Gunicorn

FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Set work directory
WORKDIR /app

# Copy only dependency files first
COPY pyproject.toml poetry.lock ./

# Install dependencies without creating a virtualenv
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy rest of the project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port (optional for Render)
EXPOSE 8000

# Start with Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--log-file", "-"]