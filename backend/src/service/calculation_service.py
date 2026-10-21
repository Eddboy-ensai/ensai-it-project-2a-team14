import pandas as pd
import math
from business_object.station import Station
from dao.station_record_dao import StationRecordDao
from utils.log_utils import log


class CalculationService:
    def __init__(self, station: Station):
        self.station = station
        self.station_records = StationRecordDao.list_all_by_id(station.id_station)

    @log
    def compute_fill_rate(self) -> float:
        """Calculate what fraction of the station is actually filled.

        Returns :
        ---------
        float
             the fraction of the station actually filled
        """
        if not self.station or self.station.capacity == 0 or self.station.capacity is None:
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
        shortage_start = None
        for records in sorted_records:
            if records.nb_available_spaces == self.station.capacity:
                if shortage_start is None:
                    shortage_start = records.date
            elif shortage_start is not None:
                total_time += (records.date - shortage_start).total_seconds()
                number_of_shortage += 1
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
        saturation_start = None
        for records in sorted_records:
            if records.nb_available_spaces == 0:
                if saturation_start is None:
                    saturation_start = records.date
            elif saturation_start is not None:
                total_time += (records.date - saturation_start).total_seconds()
                number_of_saturation += 1
        if number_of_saturation == 0:
            return 0.0
        saturation_mean_time = total_time / number_of_saturation
        return saturation_mean_time

    @log
    def compute_sat_score(self) -> float:
        """Calculate the saturation score of the station based on saturation mean time, and saturation rate

        Returns :
        ---------
        float
            the saturation score of the station
        """
        a = 0.5
        t = 3600
        Tsat = self.compute_saturation_rate
        Dsat = self.compute_saturation_mean_time
        dsat = 1 - math.exp(-Dsat / t)
        sat_score = round(Tsat ** (1 - a) * dsat ** a)
        return sat_score

    @log
    def compute_short_score(self) -> float:
        """Calculate the shortage score of the station based on shortage mean time, and shortage rate

        Returns :
        ---------
        float
            the shortage score of the station
        """
        b = 0.5
        t = 3600
        Tshort = self.compute_shortage_rate
        Dshort = self.compute_shortage_mean_time
        dshort = 1 - math.exp(-Dshort / t)
        short_score = round(Tshort ** (1 - b) * dshort ** b)
        return short_score

    @log
    def compute_score(self) -> int:
        """Calculate the fiability score of the station

        The score will be calculated using the shortage score and the saturation and some choosen parameters

        Returns :
        ---------
        float
            the fiability score of the station
        """
        c = 0.5
        d = 0.5
        score = round(100 * (1 - c * self.compute_sat_score - d * self.compute_short_score))
        return score

    @log
    def get_availability_over_time(self) -> pd.DataFrame:
        """Returns a dataframe which gives the availabilty of the station over time.

        Return :
        --------
        pd.DataFrame
            the dataframe of availability of the station over time
        """
        pass
