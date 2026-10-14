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
    id_station INTEGER PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lon DOUBLE PRECISION NOT NULL,
    capacity INTEGER
);

CREATE TABLE IF NOT EXISTS project.StationRecords (
    id_station INTEGER NOT NULL REFERENCES project.Stations(id_station),
    date TIMESTAMPTZ NOT NULL,
    status VARCHAR(50),
    nb_available_spaces INTEGER,
    nb_available_bikes INTEGER,
    nb_available_ebikes INTEGER,
    PRIMARY KEY (id_station, date)
);

CREATE TABLE IF NOT EXISTS project.Favorites (
    id_user INTEGER REFERENCES project.Users(id_user),
    id_station INTEGER REFERENCES project.Stations(id_station),
    PRIMARY KEY (id_user, id_station)
);

CREATE INDEX IF NOT EXISTS idx_station_records_date ON project.StationRecords(date);

INSERT INTO project.Users(username, pwdh, admin) VALUES
('jojo', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', true),
('mimi', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', false),
('fafa', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', false),
('beber', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', false);

INSERT INTO project.Stations(id_station, name, lat, lon, capacity) VALUES
(5501, 'République', -1.678037, 48.110026, 45),
(5502, 'Mairie-Opéra', -1.678757, 48.111624, 24),
(5504, 'Place Hoche', -1.677073, 48.115074, 39),
(5505, 'Sainte-Anne', -1.680534, 48.114219, 24);



INSERT INTO project.StationRecords(
  id_station,
  date,
  status,
  nb_available_spaces,
  nb_available_bikes,
  nb_available_ebikes
)
VALUES
(5501, '2026-10-13 08:00:00+02', 'IN_SERVICE', 25, 10, 10),
(5501, '2026-10-13 08:15:00+02', 'IN_SERVICE', 20, 15, 10),
(5501, '2026-10-13 08:30:00+02', 'IN_SERVICE', 10, 25, 10),
(5501, '2026-10-13 08:45:00+02', 'IN_SERVICE', 0, 35, 10),
(5501, '2026-10-13 09:00:00+02', 'IN_SERVICE', 0, 35, 10),
(5501, '2026-10-13 09:15:00+02', 'IN_SERVICE', 0, 35, 10),
(5501, '2026-10-13 09:30:00+02', 'IN_SERVICE', 0, 35, 10),
(5501, '2026-10-13 09:45:00+02', 'IN_SERVICE', 0, 35, 10),
(5501, '2026-10-13 10:00:00+02', 'IN_SERVICE', 0, 35, 10),
(5502, '2026-10-13 08:00:00+02', 'IN_SERVICE', 24, 0, 0),
(5502, '2026-10-13 08:15:00+02', 'IN_SERVICE', 24, 0, 0),
(5502, '2026-10-13 08:30:00+02', 'IN_SERVICE', 24, 0, 0),
(5502, '2026-10-13 08:45:00+02', 'IN_SERVICE', 24, 0, 0),
(5502, '2026-10-13 09:00:00+02', 'IN_SERVICE', 19, 5, 0),
(5502, '2026-10-13 09:15:00+02', 'IN_SERVICE', 13, 11, 0),
(5502, '2026-10-13 09:30:00+02', 'IN_SERVICE', 9, 15, 0),
(5502, '2026-10-13 09:45:00+02', 'IN_SERVICE', 11, 13, 0),
(5502, '2026-10-13 10:00:00+02', 'IN_SERVICE', 11, 13, 0),
(5504, '2026-10-13 08:00:00+02', 'IN_SERVICE', 13, 13, 13),
(5504, '2026-10-13 08:15:00+02', 'IN_SERVICE', 15, 14, 10),
(5504, '2026-10-13 08:30:00+02', 'IN_SERVICE', 21, 8, 10),
(5504, '2026-10-13 08:45:00+02', 'IN_SERVICE', 32, 0, 7),
(5504, '2026-10-13 09:00:00+02', 'IN_SERVICE', 34, 0, 5),
(5504, '2026-10-13 09:15:00+02', 'IN_SERVICE', 36, 0, 3),
(5504, '2026-10-13 09:30:00+02', 'IN_SERVICE', 33, 3, 3),
(5504, '2026-10-13 09:45:00+02', 'IN_SERVICE', 31, 5, 3),
(5504, '2026-10-13 10:00:00+02', 'IN_SERVICE', 31, 5, 3),
(5505, '2026-10-13 08:00:00+02', 'NOT_INSTALLED', 0, 0, 0),
(5505, '2026-10-13 08:15:00+02', 'NOT_INSTALLED', 0, 0, 0),
(5505, '2026-10-13 08:30:00+02', 'NOT_INSTALLED', 0, 0, 0),
(5505, '2026-10-13 08:45:00+02', 'NOT_INSTALLED', 0, 0, 0),
(5505, '2026-10-13 09:00:00+02', 'NOT_INSTALLED', 0, 0, 0),
(5505, '2026-10-13 09:15:00+02', 'NOT_INSTALLED', 0, 0, 0),
(5505, '2026-10-13 09:30:00+02', 'NOT_INSTALLED', 0, 0, 0),
(5505, '2026-10-13 09:45:00+02', 'NOT_INSTALLED', 0, 0, 0),
(5505, '2026-10-13 10:00:00+02', 'NOT_INSTALLED', 0, 0, 0);

INSERT INTO project.Favorites(
  id_user,
  id_station
)
VALUES
(1, 5501),
(1, 5502),
(2, 5504),
(4, 5504),
(4, 5505);