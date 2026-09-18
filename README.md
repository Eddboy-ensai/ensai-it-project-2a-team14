# ensai-it-project-2a-team14

1) Create a PostgreSQL service, a .env file and complete the following variables :

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


2) In a terminal, execute `uv run --project backend python backend/src/main.py`