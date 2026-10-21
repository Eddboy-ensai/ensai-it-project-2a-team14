from business_object.station import Station
from dao.station_record_dao import StationRecordDao
from utils.log_utils import log
from calculation_service import CalculationService


class SuggestionScore:
    def __init__(self, station: Station):
        self.station = station

    @log
    def station_pick_suggestion_score(self) -> int:
        """Compute the "pick suggestion score" of the station the user selected

        Return :
        ---------
        int
            The "pick suggestion score" of the station
        """
        pass

    @log
    def station_drop_suggestion_score(self) -> int:
        """Compute the "drop suggestion score" of the station the user selected

        Return :
        ---------
        int
            The "drop suggestion score" of the station
        """
        pass

    @log
    def is_recommended_pick(self) -> bool:
        """Tell based on pick suggestion score of the choosen station if we recommend it or not

        Return :
        --------
        bool
            1 if the pick suggestion score is high enough, 0 if not
        """
        pass

    @log
    def is_recommended_drop(self) -> bool:
        """Tell based on drop suggestion score of the choosen station if we recommend it or not

        Return :
        --------
        bool
            1 if the drop suggestion score is high enough, 0 if not
        """
        pass

    @log
    def get_suggestion_pick(self) -> list(Station):
        """Select the suggested stations around

        Select all the stations in a close area around the choosen station and with at least 2 available bikes which  have a better pick suggestion score than the one of the station choosen by the user (station_pick_suggestion_score)

        Return :
        --------
        list(Station)
            The list of the recommended stations
        """
        pass

    @log
    def get_suggestion_drop(self) -> list(Station):
        """Select the suggested stations around

        Select all the stations in a close area around the choosen station and with at least 2 available spots which  have a better drop suggestion score than the one of the station choosen by the user (station_drop_suggestion_score)

        Return :
        --------
        list(Station)
            The list of the recommended stations
        """
        pass