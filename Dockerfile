FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# ENV POETRY_HOME="/opt/poetry"
# ENV PATH="$POETRY_HOME/bin:$PATH"

# Install Poetry
RUN pip install poetry
# Set the working directory in the container
WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copy the rest of the application code into the container
COPY . .

# Make port 8000 available to the world outside this container
# Change this if your Django application runs on a different port
# EXPOSE 8000

# Run your Django application
# This command uses the development server for demonstration.
# For production, you should use a production-ready WSGI server like Gunicorn or uWSGI.
# Example for Gunicorn: CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project_name.wsgi:application"]
CMD ["poetry","run","python", "manage.py", "runserver", "0.0.0.0:8000"]
