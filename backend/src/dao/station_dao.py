from business_object.station import Station
from dao.db_connection import DBConnection
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class StationDao(metaclass=Singleton):
    @log
    def upsert_all(self, stations: list[Station]) -> int:
        """Insert new stations or update existing ones.
        Parameters
        ----------
        stations: list[Station]
            stations to insert or update
        Returns
        -------
        int
            number of rows inserted or updated
        """
        if not stations:
            return 0

        nb_rows = 0
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    for station in stations:
                        cursor.execute(
                            "INSERT INTO project.Stations"
                            "(id_station, name, lat, lon, capacity) "
                            "VALUES (%(id_station)s, %(name)s, %(lat)s, "
                            "        %(lon)s, %(capacity)s) "
                            "ON CONFLICT (id_station) DO UPDATE SET "
                            "    name     = EXCLUDED.name, "
                            "    lat      = EXCLUDED.lat, "
                            "    lon      = EXCLUDED.lon, "
                            "    capacity = EXCLUDED.capacity;",
                            vars(station),
                        )
                        nb_rows += cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return nb_rows

    def find_by_id(self, id_station: int) -> Station:
        """Find a station by its id.
        Parameters
        ----------
        id_station : int
            The ID of the station to find
        Returns
        -------
            Station matching the given id
        """
        pass

    def list_all(self) -> list[Station]:
        """List all stations found in the database
        Returns
        -------
        list[Station]
            list of all the users
        """
        pass
