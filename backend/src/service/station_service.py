from business_object.station import Station
from dao.station_dao import StationDao
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
        list[Station]:
            list of all the stations
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
