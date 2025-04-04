# Microservice Boilerplate (Python)

Welcome to the **Microservice Boilerplate** repository. This template is designed to streamline the creation of new Python-based microservices, incorporating:

- **gRPC** for high-performance communication
- **SQLAlchemy** for database interactions
- **Alembic** for database migrations
- **Redis** for caching or messaging
- **Logging** (using Python's built-in `logging` or a similar library)
- **Pydantic** for data validation
- **Poetry** for dependency management

---

## Creating a New Service from This Template

When you generate a new microservice from this repository, follow these steps to tailor it to your project:

1. **Rename the Service**

   - Update all references from `boilerplate-ms-python` (or any existing placeholder name) to your desired service name (e.g., `user-service`).
   - Common places to check:
     - `pyproject.toml` (project name, dependencies, etc.)
     - Any references in this README or other documentation

> [!IMPORTANT]
> Rename the folder inside `src/` and update all the imports

2. **Review Alembic Migrations**

   - If your project requires database migrations, edit or replace the default Alembic files and run:
     ```bash
     alembic upgrade head
     ```
     to ensure your database schema is up-to-date.

3. **Check Environment Variables**
   - Make sure environment variables (e.g., database connection strings, Redis configuration) match your new microservice’s requirements.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Setup and Usage](#setup-and-usage)
3. [Debugging](#debugging)
4. [Scripts Overview](#scripts-overview)
5. [Testing and Coverage](#testing-and-coverage)
6. [Environment Variables](#environment-variables)

---

## Project Structure

```
boilerplate-ms-python/
├─ .vscode/
├─ migrations/         # Alembic migrations (if using Alembic)
├─ src/
│  ├─ config/
│  ├─ enums/
│  ├─ proto_generated/  # Generated artifacts
│  ├─ protos/           # .proto files
│  ├─ repositories/
│  ├─ services/
│  ├─ utilities/
│  ├─ dev_runner.py     # Enables hot-reload and debugpy
│  └─ main.py           # Main entry point of the app
└─ tests/
```

- `src/` contains all Python source files.
- `migrations/` holds Alembic migration scripts (if you’re using Alembic).
- `tests/` contains your test suite.
- `pyproject.toml` manages dependencies (via Poetry).

---

## Setup and Usage

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd boilerplate-ms-python
   ```

2. **Run ./setup init**  
   To install all poetry dependencies and activate your .venv you will
   need to run this in your terminal:

   ```
   ./setup.sh init
   ```

   This will activate your python .venv in your terminal, and now you can use any package CLI installed from poetry dependencies

3. **Build and Run via Command Line**  
   Build and run the containers directly from a terminal:

   ```bash
   docker compose up --build -d
   ```

   This command will build the Docker images, then run them in detached mode.

> [!NOTE]  
> **Rebuilding Docker Image**  
>  You will only need to rebuild the image if you're adding any dependency to the project.

### Environment Variables

- **Local `.env` File**  
  Docker Compose will automatically use environment variables from your local `.env` file (located in the same directory as the `docker-compose.yml`), ensuring the service and its dependencies share the same configuration.

---

## Debugging

- **VSCode Debug Attach**  
  If you need to debug the service while it’s running in Docker, open the **Run and Debug** panel in VSCode, select the **“docker-compose: attach”** configuration, and start debugging.

- **Hot Reload and Debugger Attachments**  
  When using hot reload in Python (e.g., via `uvicorn --reload`), **any time code changes**, the process restarts. This can **disconnect** the debugger, so you may need to re-attach after each reload event.

---

## Scripts Overview

- **`./setup.sh init`**  
  Installs dependencies via Poetry and generates gRPC stubs from `.proto` files.

- **`./setup.sh proto`**  
  Re-generates gRPC services/messages from `.proto` files (if you modify them after the initial setup).

- **`./setup.sh init-docker`**  
  Re-generates gRPC services/messages from `.proto` files (if you modify them after the initial setup).

---

## Testing and Coverage

- All tests reside in the `tests/` directory.
- If you’re using `pytest` with coverage, run:
  ```bash
  poetry run pytest --cov=src tests/
  ```
- **Coverage** should remain above **85%**. Configure your test commands or CI pipeline to verify coverage automatically.

---

## Environment Variables

Make sure to set the following environment variables for smooth operation (adjust as needed for your setup):

- `DATABASE_URL_PYTHON` (or a name of your choosing): Connection string for your database (SQLAlchemy).
- `REDIS_HOST`: Host address for Redis.
- `REDIS_PORT`: Port used by Redis.
- `REDIS_PASSWORD`: Password for Redis (if applicable).
- `LOGGING_LEVEL`: Logging level (`INFO`, `DEBUG`, `ERROR`, etc.).
- `PYTHON_ENV`: Environment identifier (e.g., `dev`, `prd`).
