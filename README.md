# **Django Backend Template**

Ready-to-use template for robust Django backend services.
Features Docker, Poetry, Sentry, and is optimized for cloud deployment (e.g., Render).

## **✨ Features**

- Dockerized: Consistent dev & prod environments with `docker-compose`.
- Modern Python: Poetry for dependency management.
- API Ready: Django REST Framework + `drf-spectacular` for auto-docs (Swagger UI/Redoc).
- Error Tracking: Integrated Sentry for production monitoring.
- Modular: Scalable `apps/` structure.
- Ops Friendly: `Makefile` for streamlined development & deployment tasks.


## **Prerequisites**

* Docker and Docker Compose installed on your system.
* Python 3.12 installed (for local development if not using Docker exclusively).
* Poetry installed (for local development if not using Docker exclusively).

## **🚀 Get Started**
- Clone:
    ```bash
    git clone <repository_url>
    cd django-template
    ```
- Environments: Create `.env.dev` (local) and `.env.prod` (production - DO NOT COMMIT) from .env.example.
- Develop Locally:
    ```bash
    make build-dev # Build image
    make up-dev    # Start app & DB
    ```
    Access: http://localhost:8000/ (App), http://localhost:8000/ (Docs).

## **🗂️ Project Structure**
```bash
.
├── apps/                    # Your Django applications (modular design)
├── config/                  # Core Django setup (settings, URLs, WSGI, ASGI, Gunicorn, Logging)
│   ├── settings/            # Environment-specific Django settings (base, dev, prod)
│   ├── gunicorn_conf.py     # Production WSGI server config
│   └── logging_config.py    # Centralized logging with Sentry
├── .env.*.example           # Environment variable templates
├── Dockerfile               # Production-ready Docker build
├── Makefile                 # Automation script for common dev/ops tasks
├── docker-compose.dev.yml   # Local development setup (app + PostgreSQL)
├── docker-compose.prod.yml  # Production deployment setup
├── manage.py                # Django CLI utility
├── poetry.lock              # Locked dependencies for reproducible builds
└── pyproject.toml           # Poetry project definition & dependencies
```

## **🛠️ Key Makefile Commands**

- make build-dev/prod: Build Docker images.
- make up-dev/prod: Start services.
- make down-dev/prod: Stop services.
- make logs-dev/prod: View logs.
- make migrate-dev: Run migrations.
- make createsuperuser-dev: Create admin user.
- make shell-dev: Access container shell.