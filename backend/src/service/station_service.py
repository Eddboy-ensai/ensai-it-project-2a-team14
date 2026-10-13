import pandas as pd

from business_object.favorite import Favorite
from business_object.station import Station
from dao.favorite_dao import FavoriteDao
from dao.station_dao import StationDao
from service.calculation_service import CalculationService
from utils.log_utils import log


class StationService:
    @log
    def find_by_id(self, id_station: int) -> Station | None:
        """Finds a specific station by its unique id.
        Parameters
        ----------
        id_station: int
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
    def get_stats(self, station: Station) -> list[float]:
        """Get the statistics of a station by asking the methods of the class StationCalculationService
        Parameters
        ----------
        station: Station
            the station from which we want to get the statistics
        Returns
        -------
        list[float]
            list of all the statistics
        """
        fill_rate = CalculationService().compute_fill_rate()
        shortage_rate = CalculationService().compute_shortage_rate()
        saturation_rate = CalculationService().compute_saturation_rate()
        shortage_mean_time = CalculationService().compute_shortage_mean_time()
        saturation_mean_time = CalculationService().compute_saturation_mean_time()
        return [fill_rate, shortage_rate, saturation_rate, shortage_mean_time, saturation_mean_time]

    @log
    def get_availibility_over_time(self, station: Station, range: int) -> pd.DataFrame:
        """Call the method of the DAO to get availibility over time of a station.
        Parameters
        ----------
        station: Station
            Station from which we want the avaibility
        range : int
            Range of time
        Returns
        -------
        pd.DataFrame
            the dataframe containing availibilities

        """
        pass

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
        pass
