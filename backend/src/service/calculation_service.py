from business_object.station import Station
from controller.station_controller import StationController
from dao.station_dao import StationDao
from business_object.station_record import StationRecord
from dao.station_record_dao import StationRecordDao
from utils.log_utils import log
import matplotlib.pyplot as plt
from plt.figure import Figure


class CalculationService:
    def __init__(
        self,
        station: Station
        ):
        self.station_records = StationRecordDao.list_all_by_id(station.id_station)

    @log
    def compute_fill_rate(self) -> float:
        """Calculate what fraction of the station is actually filled.

        Retruns :
        ---------
        float
             the fraction of the station actually filled
        """
        pass

    @log
    def compute_shortage_rate(self) -> float:
        """Calculate the percentage of time where the station is empty.

        Returns :
        ---------
        float
            the percentage of the time where the station is empty
        """
        pass

    @log
    def compute_saturation_rate(self) -> float:
        """Calculate the percentage of time where the station is full.

        Returns :
        ---------
        float
            the percentage of the time where the station is full
        """
        pass

    @log
    def compute_shortage_mean_time(self) -> float:
        """Calculate the mean time of the episodes of shortage.

        Returns :
        ---------
        float
            mean time of the episodes of shortage
        """
        pass

    @log
    def compute_saturation_mean_time(self) -> float:
        """Calculate the mean time of the episodes of saturation.

        Returns :
        ---------
        float
            mean time of the episodes of saturation
        """
        pass

    @log
    def get_availability_over_time(self) -> Figure:
        """Plot a figure which represent the availabilty of the station over time.

        Return :
        --------
        Figure
            the availability of the station over time plotted
        """
        pass

    @log
    def compute_score(self) -> float:
        """Calculate the score of the station based on caracteristics like fiability, location etc...

        Returns :
        ---------
        float
            the score of the station
        """
        pass

    @log
    def get_suggestion(self) -> Station:
        """Find the best station for the user based on their localisation.

        Return :
        --------
        Station
            The best station station for the user based on their localisation
        """
        pass
