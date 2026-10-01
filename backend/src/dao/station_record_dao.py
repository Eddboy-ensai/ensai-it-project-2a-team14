from business_object.station_record import StationRecord
from dao.db_connection import DBConnection
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class StationRecordDao(metaclass=Singleton):
    @log
    def insert_all(self, records: list[StationRecord]) -> int:
        """Insert a batch of station records in the database.
        A record already present (same station, same date) is ignored.
        Parameters
        ----------
        records: list[StationRecord]
            records to insert
        Returns
        -------
        int
            number of rows actually inserted
        """
        if not records:
            return 0

        nb_inserted = 0
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    for record in records:
                        cursor.execute(
                            "INSERT INTO project.StationRecords"
                            "(id_station, date, status, nb_available_spaces, "
                            " nb_available_bikes, nb_available_ebikes) "
                            "VALUES (%(id_station)s, %(date)s, %(status)s, "
                            "        %(nb_available_spaces)s, %(nb_available_bikes)s, "
                            "        %(nb_available_ebikes)s) "
                            "ON CONFLICT (id_station, date) DO NOTHING;",
                            vars(record),
                        )
                        nb_inserted += cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return nb_inserted
