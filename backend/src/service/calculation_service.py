import pandas as pd

from business_object.station import Station
from dao.station_record_dao import StationRecordDao
from utils.log_utils import log


class CalculationService:
    def __init__(self, station: Station):
        self.station_records = StationRecordDao.list_all_by_id(station.id_station)

    @log
    def compute_fill_rate(self) -> float:
        """Calculate what fraction of the station is actually filled.

        Returns :
        ---------
        float
             the fraction of the station actually filled
        """
        if not self.station or self.station.capacity == 0:
            return 0.0
        latest_records = max(self.station_records, key=lambda r: r.date, default=None)
        if not latest_records:
            return 0.0
        filled_spaces = latest_records.nb_available_bikes + latest_records.nb_available_ebikes
        filled_rate = filled_spaces / self.station.capacity
        return filled_rate

    @log
    def compute_shortage_rate(self) -> float:
        """Calculate the percentage of time where the station is empty.

        Returns :
        ---------
        float
            the percentage of the time where the station is empty
        """
        if not self.station_records or len(self.station_records) < 2:
            return 0.0
        sorted_records = sorted(self.station_records, key=lambda r: r.date)
        total_duration = 0.0
        empty_duration = 0.0
        for i in range(len(sorted_records) - 1):
            current_record = sorted_records[i]
            next_record = sorted_records[i + 1]

            interval_time = (next_record.date - current_record.date).total_seconds()

            total_duration += interval_time

            if current_record.nb_available_spaces == self.station.capacity:
                empty_duration += interval_time
        if total_duration == 0:
            return 0.0
        shortage_rate = empty_duration / total_duration
        return shortage_rate

    @log
    def compute_saturation_rate(self) -> float:
        """Calculate the percentage of time where the station is full.

        Returns :
        ---------
        float
            the percentage of the time where the station is full
        """
        if not self.station_records or len(self.station_records) < 2:
            return 0.0
        sorted_records = sorted(self.station_records, key=lambda r: r.date)
        total_duration = 0.0
        empty_duration = 0.0
        for i in range(len(sorted_records) - 1):
            current_record = sorted_records[i]
            next_record = sorted_records[i + 1]

            interval_time = (next_record.date - current_record.date).total_seconds()

            total_duration += interval_time

            if current_record.nb_available_spaces == 0:
                empty_duration += interval_time
        if total_duration == 0:
            return 0.0
        saturation_rate = empty_duration / total_duration
        return saturation_rate

    @log
    def compute_shortage_mean_time(self) -> float:
        """Calculate the mean time of the episodes of shortage.

        Returns :
        ---------
        float
            mean time of the episodes of shortage
        """
        if not self.station_records or len(self.station_records) < 2:
            return 0.0
        sorted_records = sorted(self.station_records, key=lambda r: r.date)
        number_of_shortage = 0.0
        total_time = 0.0
        index_of_the_last_time_the_shortage_period_started = 0
        index_of_the_last_time_the_shortage_period_ended = 0
        for i in range(len(sorted_records) - 1):
            if (
                not index_of_the_last_time_the_shortage_period_started
                < i
                < index_of_the_last_time_the_shortage_period_ended
            ):
                if sorted_records[i].nb_available_spaces == self.station.capacity:
                    time = 0
                    index_of_the_last_time_the_shortage_period_started = i
                    while sorted_records[i].nb_available_spaces == self.station.capacity:
                        i += 1
                    time += (sorted_records[i + 1].date - sorted_records[i].date).total_seconds()
                    total_time += time
                    number_of_shortage += 1
                    index_of_the_last_time_the_shortage_period_ended = i + 1
        if number_of_shortage == 0:
            return 0.0
        shortage_mean_time = total_time / number_of_shortage
        return shortage_mean_time

    @log
    def compute_saturation_mean_time(self) -> float:
        """Calculate the mean time of the episodes of saturation.

        Returns :
        ---------
        float
            mean time of the episodes of saturation
        """
        if not self.station_records or len(self.station_records) < 2:
            return 0.0
        sorted_records = sorted(self.station_records, key=lambda r: r.date)
        number_of_saturation = 0.0
        total_time = 0.0
        index_of_the_last_time_the_saturation_period_started = 0
        index_of_the_last_time_the_saturation_period_ended = 0
        for i in range(len(sorted_records) - 1):
            if (
                not index_of_the_last_time_the_saturation_period_started
                < i
                < index_of_the_last_time_the_saturation_period_ended
            ):
                if sorted_records[i].nb_available_spaces == 0:
                    time = 0
                    index_of_the_last_time_the_saturation_period_started = i
                    while sorted_records[i].nb_available_spaces == 0:
                        i += 1
                    time += (sorted_records[i + 1].date - sorted_records[i].date).total_seconds()
                    total_time += time
                    number_of_saturation += 1
                    index_of_the_last_time_the_saturation_period_ended = i + 1
        if number_of_saturation == 0:
            return 0.0
        saturation_mean_time = total_time / number_of_saturation
        return saturation_mean_time

    @log
    def get_availability_over_time(self) -> pd.DataFrame:
        """Returns a dataframe which gives the availabilty of the station over time.

        Return :
        --------
        pd.DataFrame
            the dataframe of availability of the station over time
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
