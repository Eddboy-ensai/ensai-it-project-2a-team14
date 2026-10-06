from business_object.Favorite import Favorite
from business_object.Station import Station
from plt.figure import Figure

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
        pass

    @log
    def list_all(self) -> list[Station]:
        """Retrieves all stations from the database by asking to the dao
        Returns
        --------
            list[Station]
        """
        pass

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
        pass

    @log
    def get_availibility_over_time(self, station: Station, range: int) -> Figure:
        """Call the method of the DAO to get availibility over time of a station.
        Parameters
        ----------
        station: Station
            Station from which we want the avaibility
        range : int
            Range of time
        Returns
        -------
        Figure
            availibility

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
        pass

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
        pass

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
