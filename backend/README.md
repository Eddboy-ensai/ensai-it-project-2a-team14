
# Backend - Engine API

This is the core engine of the application. It is a layered REST API built with [FastAPI](https://fastapi.tiangolo.com/), responsible for collecting bike station data from and external GBFS API, computing statistics, reliability scores and recomandations and managing users and their favorite stations.

## 🚀 Run the application

The full installation procedure (PostgreSQL service, .env file and frontend) is described in the [main README](../README.md). All commands below are run from the repository's root directory.

- `init_db.py` (`uv run --project backend python backend/src/init_db.py`) : creates the tables and the first administrator (from `ADMIN_USERNAME` and `ADMIN_PASSWORD`)
- `collector.py` (`uv run --project backend python backend/src/collector.py`) : collects station data every 5 minutes, must be kept running
- `main.py` (`uv run --project backend python backend/src/main.py`) : starts the API on port 5000. The swagger is available on `/docs`.
- `export_db.py` (`uv run --project backend python backend/src/export_db.py`) : saves the content of the database in `data/backup_db.sql` (while backup_db.sql is in the gitignore it musn't be published as it contains the hashed passwords and connexion tokens)


## 🏛️ Architecture

The backend follows a **Layered Architecture** to ensure separation of concerns and maintainability:

- **Business Object** (`business_object/`) : Represents the pure domain entities
- **Controller** (`controller/`) : Handles HTTP requests and routing via FastAPI
- **Service** (`service/`) : Contains the core business logic
- **DAO** (`dao/`) : Manages database interactions
- **Schema** (`schema/`) : Data contract via [Pydantic](https://pydantic.dev/docs/validation/latest/get-started/) to ensure API requests and responses follow a strict structure
- **Utils** (`utils/`): security (password hashing, token verification), logging, environment variables and the `Singleton` metaclass used by the DAO classes


## ⚒️ Development toolkit

### Debugging & Logs

The application uses a structured logging system. Logs are written to the `backend/logs/` directory and follow the format defined in `logging_config.yml`.

A custom `@log` decorator is available to automatically log method inputs and outputs, making it easier to trace the flow of data through the services.

### Unit tests

The tests cover the service layer. They require a reachable database: a valid `.env` file and the tables created with `init_db.py`.


Command to run from the repository's root directory:  

- Install dependencies : `uv sync --project backend --extra dev`  
- Execute the tests : `uv run --project backend pytest -v`