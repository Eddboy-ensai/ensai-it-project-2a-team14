from datetime import UTC, datetime

from business_object.station_record import StationRecord
from dao.station_record_dao import StationRecordDao

from business_object.station import Station
from dao.gbfs_dao import GbfsDao
from dao.station_dao import StationDao
from utils.log_utils import log


class CollectService:

    @log
    def refresh_stations(self) -> int:
        """Fetches the list of stations and inserts or updates them.
        Returns
        -------
        int
            number of stations inserted or updated
        """
        raw = GbfsDao().get_station_information()
        stations = self.extract_stations(raw)
        return StationDao().upsert_all(stations)

    @staticmethod
    def extract_stations(raw: dict) -> list[Station]:
        """Converts the GBFS station_information JSON into Station objects."""
        return [
            Station(
                id_station=s["station_id"],
                name=s["name"],
                lat=s["lat"],
                lon=s["lon"],
                capacity=s.get("capacity"),
            )
            for s in raw["data"]["stations"]
        ]

    @log
    def collect_records(self) -> int:
        """Fetches the current status of all stations and stores it."""
        raw = GbfsDao().get_station_status()
        records = self.extract_records(raw)
        return StationRecordDao().insert_all(records)

    @staticmethod
    def extract_records(raw: dict) -> list[StationRecord]:
        """Converts the GBFS station_status JSON into StationRecord objects.
        All records of one call share the same date.
        """
        date = datetime.now(UTC)
        return [
            StationRecord(
                id_station=s["station_id"],
                date=date,
                status=CollectService._compute_status(s),
                nb_available_spaces=s["num_docks_available"],
                nb_available_bikes=s["num_bikes_available"],
                nb_available_ebikes=s.get("num_ebikes_available"),
            )
            for s in raw["data"]["stations"]
        ]

    @staticmethod
    def _compute_status(s: dict) -> str:
        """Builds a readable status from the GBFS boolean flags."""
        if not s.get("is_installed", True):
            return "NOT_INSTALLED"
        if not s.get("is_renting", True):
            return "NOT_RENTING"
        if not s.get("is_returning", True):
            return "NOT_RETURNING"
        return "IN_SERVICE"
