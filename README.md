# ensai-it-project-2a-team14

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
7) Go to the swagger (Onyxia -> Mes services -> click on "ouvrir" on the project vscode service -> click on "port 5000") or use the webservice ("port 8000" after executing, in a terminal the commands `cd frontend` and `uv run --project . streamlit run src/app.py`)  
8) To execute the test :  
`uv sync --project backend --extra dev` (to install dependencies)  
`uv run --project backend pytest -v`(to execute the tests)  