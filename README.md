# VeloScope  

VeloScope is an application that provides services related to bike stations in a city. It allows users to access real-time information, historical data and predictions. Using this application requires creating an account.  

## Run the application  

The following steps are described to ensure its deployment on SSP cloud (Onyxia).

Commands are to be run from the repository's root directory (steps 1 and 4 are optional if you already have a database):

1) In Onyxia create a PostgreSQL service
- Onyxia -> Mes services -> click on + Nouveau service -> Postgresql-cnpg -> Lancer -> Lancer
2) Create a file named `.env` file in the root of the project and complete the following variables (marked with <...>), where ADMIN_USERNAME and ADMIN_PASSWORD are the username and password you have chosen for the first Administrator while the PostgreSQL variables can be found by clicking on the service Postgres:  

```default
POSTGRES_HOST=<postgresql-cnpg-suffix>
POSTGRES_PORT=5432
POSTGRES_DATABASE=defaultdb
POSTGRES_USER=<user-username>
POSTGRES_PASSWORD=<password>
POSTGRES_SCHEMA=project

UVICORN_HOST=0.0.0.0
UVICORN_PORT=5000

BACKEND_URL=http://localhost:5000
BACKEND_TIMEOUT=5

ADMIN_USERNAME=<admin username>
ADMIN_PASSWORD=<admin password>
```


3) Install dependencies by executing `uv sync --project backend` and `uv sync --project frontend`  
4) Create empty schemas and the first administrator by running: `uv run --project backend python backend/src/init_db.py`  
5) Run in a new terminal to collect data (do not stop it): `uv run --project backend python backend/src/collector.py`  
6) In a new terminal, execute `uv run --project backend python backend/src/main.py` (Must be kept running.)
7) You can then use the application with the Swagger through port 5000 on Onyxia 
- Onyxia -> Mes services -> click on "ouvrir" on the project vscode service -> click on "port 5000"
8) In order to use the webservice:  
- run the following commands in a new terminal `cd frontend` and `uv run --project . streamlit run src/app.py`  
- Onyxia -> Mes services -> click on "ouvrir" on the project vscode service -> click on "port 8000"
9) You can then create an account or login as the super Administrator with the login credentials you used.


## Back up the database

`uv run --project backend python backend/src/export_db.py` saves the content of the database in `data/backup_db.sql`.
