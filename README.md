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

3) Create the schema project and the table Users by executing this code (for example in cloudbeaver) :
```default
CREATE SCHEMA project;

CREATE TABLE project.Users (
    id_user SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    pwdh VARCHAR(255) NOT NULL,
    admin BOOLEAN NOT NULL DEFAULT FALSE,
    access_token VARCHAR(255)
);
```

4) Create the tables Stations and StationRecords by executing this code :
```default
CREATE TABLE project.Stations (
    id_station VARCHAR(50) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    capacity INTEGER
);

CREATE TABLE project.StationRecords (
    id_station VARCHAR(50) NOT NULL REFERENCES project.Stations(id_station),
    date TIMESTAMPTZ NOT NULL,
    status VARCHAR(50),
    nb_available_spaces INTEGER,
    nb_available_bikes INTEGER,
    nb_available_ebikes INTEGER,
    PRIMARY KEY (id_station, date)
);

CREATE INDEX idx_station_records_date ON project.StationRecords(date);
```


5) Install dependencies by executing `uv sync --project backend`
6) In a terminal, execute `uv run --project backend python backend/src/main.py`
7) Go to the swagger (Onyxia -> Mes services -> click on "ouvrir" on the project vscode service -> click on "port 5000") or use the webservice ("port 8000" after executing, in a terminal the commands `cd frontend` and `uv run --project . streamlit run src/app.py`)