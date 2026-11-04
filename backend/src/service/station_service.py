from business_object.favorite import Favorite
from business_object.station import Station
from business_object.station_record import StationRecord
from dao.favorite_dao import FavoriteDao
from dao.station_dao import StationDao
from dao.station_record_dao import StationRecordDao
from service.calculation_service import CalculationService
from utils.log_utils import log


class StationService:
    @log
    def find_by_id(self, id_station: str) -> Station | None:
        """Finds a specific station by its unique id.
        Parameters
        ----------
        id_station: str
            The ID of the station
        Returns
        -------
        Station:
            Station object if found, otherwise None.
        """
        return StationDao().find_by_id(id_station)

    @log
    def list_all(self) -> list[Station]:
        """Retrieves all stations from the database by asking to the dao
        Returns
        --------
            list[Station]
        """
        return StationDao().list_all()

    @log
    def get_stats(self, station: Station) -> dict:
        """Get the statistics of a station by asking the methods of the class StationCalculationService
        Parameters
        ----------
        station: Station
            the station from which we want to get the statistics
        Returns
        -------
        dict
            dictionary of all the informations and statistics about a station
        """
        calculation_service = CalculationService(station)
        fill_rate = calculation_service.compute_fill_rate()
        shortage_rate = calculation_service.compute_shortage_rate()
        saturation_rate = calculation_service.compute_saturation_rate()
        shortage_mean_time = calculation_service.compute_shortage_mean_time()
        saturation_mean_time = calculation_service.compute_saturation_mean_time()
        return {
            "fill_rate": fill_rate,
            "shortage_rate": shortage_rate,
            "saturation_rate": saturation_rate,
            "shortage_mean_time": shortage_mean_time,
            "saturation_mean_time": saturation_mean_time,
        }

    @log
    def get_availability_over_time(self, station: Station, nb_days: int) -> list[StationRecord]:
        """Returns the records of a station over the last n days, sorted by date.
        Parameters
        ----------
        station: Station
            Station from which we want the availability
        nb_days : int
            Number of days to look back (e.g. 1, 7 or 30)
        Returns
        -------
        list[StationRecord]
            the records of the station since now - nb_days
        """
        return StationRecordDao().list_last_days_by_id(station.id_station, nb_days)

    @log
    def favorite_already_exists(self, favorite: Favorite) -> bool:
        """Check if a favorite already exists in the databse.
        Parameters
        ----------
        favorite : Favorite
            favorite to check
        Returns
        -------
        bool
            True if the favorite already exists in the database.
        """
        favorites = FavoriteDao().list_all()
        for fav in favorites:
            if fav.id_user == favorite.id_user and fav.id_station == favorite.id_station:
                return True
        return False

    @log
    def add_favorite(self, favorite: Favorite) -> Favorite | None:
        """Call the DAO method to add a favorite.
        Parameters
        ----------
        favorite: Favorite
            the favorite (user/station) to add
        Returns
        -------
        Favorite
            Favorite object created or None if creation failed.
        """
        created = FavoriteDao().add_favorite(favorite)
        if created:
            return favorite
        return None

    @log
    def delete_favorite(self, favorite: Favorite) -> bool:
        """Delete a favorite.
        Parameters
            Favorite object to be deleted.
        Returns
        -------
        bool
            True if deletion was successful, False otherwise.
        """
        return FavoriteDao().delete(favorite)
