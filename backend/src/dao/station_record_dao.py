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

    @log
    def list_all_by_id(id_station: int) -> list[StationRecord]:
        """List all records in the database of the choosen station.

        Parameters:
        -----------
        id_station: int
            The id of the choosen station

        Returns
        -------
        list[StationRecord]
            list of all the records of the station
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM project.StationRecords WHERE id_station=%(id_station)s",
                        {"id_station": id_station},
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        stationrecords_list = []
        if res:
            for row in res:
                stationrecord = StationRecord(
                    id_station=row["id_station"],
                    date=row["date"],
                    status=row["status"],
                    nb_available_spaces=row["nb_available_spaces"],
                    nb_available_bikes=row["nb_available_bikes"],
                    nb_available_ebikes=row["nb_available_ebikes"],
                )
                stationrecords_list.append(stationrecord)
        return stationrecords_list
