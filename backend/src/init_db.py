"""Create the database schema and tables of the project.

Usage (from the root of the repository):
    uv run --project backend python backend/src/init_db.py

The script can be run several times: existing tables are kept, with their data.
"""

from dao.db_connection import DBConnection
from utils.env_variables import load_environment_variables
from utils.log_utils import get_logger, initialize_logs

SQL_INIT = """
CREATE SCHEMA IF NOT EXISTS project;

CREATE TABLE IF NOT EXISTS project.Users (
    id_user      SERIAL PRIMARY KEY,
    username     VARCHAR(50) NOT NULL UNIQUE,
    pwdh         VARCHAR(255) NOT NULL,
    admin        BOOLEAN NOT NULL DEFAULT FALSE,
    access_token VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS project.Stations (
    id_station VARCHAR(50) PRIMARY KEY,
    name       VARCHAR(150) NOT NULL,
    lat        DOUBLE PRECISION NOT NULL,
    lon        DOUBLE PRECISION NOT NULL,
    capacity   INTEGER
);

CREATE TABLE IF NOT EXISTS project.StationRecords (
    id_station          VARCHAR(50) NOT NULL REFERENCES project.Stations(id_station),
    date                TIMESTAMPTZ NOT NULL,
    status              VARCHAR(50),
    nb_available_spaces INTEGER,
    nb_available_bikes  INTEGER,
    nb_available_ebikes INTEGER,
    PRIMARY KEY (id_station, date)
);

CREATE INDEX IF NOT EXISTS idx_station_records_date
    ON project.StationRecords(date);

CREATE TABLE IF NOT EXISTS project.Favorites (
    id_user    INTEGER NOT NULL REFERENCES project.Users(id_user) ON DELETE CASCADE,
    id_station VARCHAR(50) NOT NULL REFERENCES project.Stations(id_station),
    PRIMARY KEY (id_user, id_station)
);
"""


def init_db() -> None:
    """Executes the SQL script that creates the schema and the tables."""
    with DBConnection().connection as connection:
        with connection.cursor() as cursor:
            cursor.execute(SQL_INIT)


if __name__ == "__main__":
    initialize_logs("InitDB")
    load_environment_variables()
    logger = get_logger(__name__)

    try:
        init_db()
        logger.info("Database initialized: schema project and tables created")
        print("Database initialized: Users, Stations, StationRecords, Favorites")
    except Exception:
        logger.exception("Database initialization failed")
        raise
