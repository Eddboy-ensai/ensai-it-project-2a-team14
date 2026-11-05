from business_object.station import Station
from dao.db_connection import DBConnection
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class StationDao(metaclass=Singleton):
    @log
    def create(self, station: Station) -> bool:
        """Insert a new station in the database.
        Parameters
        ----------
        station: Station
            station to insert
        Returns
        -------
        bool
            True if the station is created, False otherwise
        """
        nb_affected_rows = 0
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO Stations(id_station, name, lat, lon, capacity) "
                        "VALUES (%(id_station)s, %(name)s, %(lat)s, %(lon)s, %(capacity)s);",
                        vars(station),
                    )
                    nb_affected_rows = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise
        return nb_affected_rows == 1

    @log
    def update(self, station: Station) -> bool:
        """Update an existing station in the database.
        Parameters
        ----------
        station: Station
            station to update, identified by its id_station
        Returns
        -------
        bool
            True if the station is updated, False otherwise
        """
        nb_affected_rows = 0
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE Stations "
                        "   SET name = %(name)s, "
                        "       lat = %(lat)s, "
                        "       lon = %(lon)s, "
                        "       capacity = %(capacity)s "
                        " WHERE id_station = %(id_station)s;",
                        vars(station),
                    )
                    nb_affected_rows = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise
        return nb_affected_rows == 1

    @log
    def find_by_id(self, id_station: str) -> Station:
        """Find a station by its id.
        Parameters
        ----------
        id_station : int
            The ID of the station to find
        Returns
        -------
            Station matching the given id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM Stations WHERE id_station = %(id_station)s; ",
                        {"id_station": id_station},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise
        station = None
        if res:
            station = Station(
                id_station=res["id_station"],
                name=res["name"],
                lat=res["lat"],
                lon=res["lon"],
                capacity=res["capacity"],
            )
        return station

    @log
    def list_all(self) -> list[Station]:
        """List all stations found in the database
        Returns
        -------
        list[Station]
            list of all the users
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM Stations")
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        stations_list = []
        if res:
            for row in res:
                station = Station(
                    id_station=row["id_station"],
                    name=row["name"],
                    lat=row["lat"],
                    lon=row["lon"],
                    capacity=row["capacity"],
                )
                stations_list.append(station)
        return stations_list
