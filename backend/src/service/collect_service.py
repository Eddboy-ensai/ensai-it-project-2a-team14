from datetime import UTC, datetime

from business_object.station import Station
from business_object.station_record import StationRecord
from dao.gbfs_dao import GbfsDao
from dao.station_dao import StationDao
from dao.station_record_dao import StationRecordDao
from utils.log_utils import log


class CollectService:
    @staticmethod
    def has_changed(old: Station, new: Station) -> bool:
        """Checks if the information of a station has changed.
        Parameters
        ----------
        old: Station
            the station as stored in the database
        new: Station
            the station as given by the GBFS feed
        Returns
        -------
        bool
            True if at least one attribute is different
        """
        return (
            old.name != new.name
            or old.lat != new.lat
            or old.lon != new.lon
            or old.capacity != new.capacity
        )

    @log
    def refresh_stations(self) -> int:
        """Fetches the list of stations, creates the new ones and updates the modified ones.
        Returns
        -------
        int
            number of stations created or updated
        """
        raw = GbfsDao().get_station_information()
        new_stations = self.extract_stations(raw)

        # Stations already in the database, indexed by id for a fast lookup
        existing = {s.id_station: s for s in StationDao().list_all()}

        nb_changes = 0
        for station in new_stations:
            if station.id_station not in existing:
                if StationDao().create(station):
                    nb_changes += 1
            elif self.has_changed(existing[station.id_station], station):
                if StationDao().update(station):
                    nb_changes += 1
        return nb_changes

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
