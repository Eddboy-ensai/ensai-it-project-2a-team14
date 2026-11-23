# Run the webservice  

The following steps are described to ensure its deployment on SSP cloud services.

Command to run from the repository's root directory (step 1 from 4 are optional if you already have a dataset):

1) Create a PostgreSQL service  
2) Create a .env file in the root of the project and complete the following variables (marked with <...>):  

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

3) Create empty schemas by running: `uv run --project backend python backend/src/init_db.py`  
4) Run in a new terminal to collect data (do not stop it): `uv run --project backend python backend/src/collector.py`  
5) Install dependencies by executing `uv sync --project backend`  
6) In a terminal, execute `uv run --project backend python backend/src/main.py`  
7) You can then use the application with the swagger  
8) In order to use the webservice :  
- run the following commands `cd frontend` and `uv run --project . streamlit run src/app.py`  
- Onyxia -> Mes services -> click on "ouvrir" on the project vscode service -> click on "port 8000"  

# Architecture

The frontend follows a modular structure to separate UI components from API interaction:

- **Pages** (`pages/`) : Individual views and user interfaces (Home, Player List, Game Play, etc.)
- **API Client** (`utils/api_client.py`) : Centralized logic for communicating with the FastAPI backend
- **Security** (`utils/auth_guard.py`) : Manages session security and token validation
- **Utilities** (`utils/`) : Helpers for logging, initialization, and common UI tasks
