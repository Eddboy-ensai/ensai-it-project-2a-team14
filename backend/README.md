
# Backend - Engine API

This is the core engine of the application. It is a layered REST API built with [FastAPI](https://fastapi.tiangolo.com/), responsible for game logic, player management, and data persistence.

## 🚀 Run the application

Command to run from the repository's root directory (step 1 from 4 are optional if you already have a dataset):

1) Create a PostgreSQL service  
2) Create a .env file in the root of the project and complete the following variables :  

```default
POSTGRES_HOST=postgresql-cnpg-<suffixe>
POSTGRES_PORT=5432
POSTGRES_DATABASE=defaultdb
POSTGRES_USER=user-<username>
POSTGRES_PASSWORD=<password>
POSTGRES_SCHEMA=project

UVICORN_HOST=0.0.0.0
UVICORN_PORT=5000

BACKEND_URL=http://localhost:5000
BACKEND_TIMEOUT=5
```

 
3) Create empty schemas by running : `uv run --project backend python backend/src/init_db.py`  
4) Run in a new terminal to collect data : `uv run --project backend python backend/src/collector.py`  
5) Install dependencies by executing `uv sync --project backend`  
6) In a terminal, execute `uv run --project backend python backend/src/main.py`  
7) Go to the swagger (Onyxia -> Mes services -> click on "ouvrir" on the project vscode service -> click on "port 5000")

## 🏛️ Architecture

The backend follows a **Layered Architecture** to ensure separation of concerns and maintainability:

- **Business Object** (`business_object/`) : Represents the pure domain entities
- **Controller** (`controller/`) : Handles HTTP requests and routing via FastAPI
- **Service** (`service/`) : Contains the core business logic
- **DAO** (`dao/`) : Manages database interactions
- **Schema** (`schema/`) : Data contract via [Pydantic](https://pydantic.dev/docs/validation/latest/get-started/) to ensure API requests and responses follow a strict structure


## ⚒️ Development toolkit

### Debugging & Logs

The application uses a structured logging system. Logs are written to the `backend/logs/` directory and follow the format defined in `logging_config.yml`.

A custom `@log` decorator is available to automatically log method inputs and outputs, making it much easier to trace the flow of data through the services.

### Unit tests

Command to run from the repository's root directory:  

- Install dependencies : `uv sync --project backend --extra dev`  
- Execute the tests : `uv run --project backend pytest -v`