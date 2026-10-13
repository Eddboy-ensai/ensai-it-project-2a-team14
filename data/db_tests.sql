/*DROP SCHEMA IF EXISTS project CASCADE;*/

CREATE SCHEMA IF NOT EXISTS project;

CREATE TABLE IF NOT EXISTS project.Users (
    id_user SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    pwdh VARCHAR(255) NOT NULL,
    admin BOOLEAN NOT NULL DEFAULT FALSE,
    access_token VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS project.Stations (
    id_station VARCHAR(50) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    capacity INTEGER
);

CREATE TABLE IF NOT EXISTS project.StationRecords (
    id_station VARCHAR(50) NOT NULL REFERENCES project.Stations(id_station),
    date TIMESTAMPTZ NOT NULL,
    status VARCHAR(50),
    nb_available_spaces INTEGER,
    nb_available_bikes INTEGER,
    nb_available_ebikes INTEGER,
    PRIMARY KEY (id_station, date)
);

CREATE INDEX IF NOT EXISTS idx_station_records_date ON project.StationRecords(date);

INSERT INTO project.Users(username, pwdh, admin) VALUES
('jojo', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', true),
('mimi', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', false);

INSERT INTO project.Stations(id_station, name, lat, lon, capacity) VALUES
(1, 'Republique', 48.8675, 2.3638, 18),
(2, 'Prefecture', 48.8584, 2.3470, 23);

INSERT INTO project.StationRecords(
  id_station,
  date,
  status,
  nb_available_spaces,
  nb_available_bikes,
  nb_available_ebikes
)
VALUES
(1, '2026-10-13 08:00:00+02', 'OPEN', 10, 5, 3),
(1, '2026-10-13 08:15:00+02', 'OPEN', 9, 6, 3),
(2, '2026-10-13 08:00:00+02', 'OPEN', 20, 1, 2),
(2, '2026-10-13 08:15:00+02', 'OPEN', 7, 11, 5);