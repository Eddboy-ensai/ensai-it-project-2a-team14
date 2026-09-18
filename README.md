# ensai-it-project-2a-team14

1) Create a PostgreSQL service

2) Create a .env file and complete the following variables :

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

3) Create the schema project and the table Users by executing this code (for example in cloudbeaver) :
```default
CREATE SCHEMA project

CREATE TABLE project.Users (
    id_user SERIAL PRIMARY KEY,
    pseudo VARCHAR(50) NOT NULL UNIQUE,
    pwdh VARCHAR(255) NOT NULL,
    admin BOOLEAN NOT NULL DEFAULT FALSE
);
```

4) Install dependies by executing `uv sync --project backend`
5) In a terminal, execute `uv run --project backend python backend/src/main.py`
6) Go to the swagger