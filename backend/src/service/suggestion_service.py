from business_object.station import Station
from dao.station_record_dao import StationRecordDao
from utils.log_utils import log
from calculation_service import CalculationService
from station_service import StationService
import math


class SuggestionScore:
    def __init__(self, station: Station):
        self.station = station

    @log
    def station_pick_suggestion_score(self) -> int:
        """Compute the "pick suggestion score" of the station the user selected

        We assume in this score than the user is located on the station, indeed the distance score values is 1 indeed dont need to appear in the formula

        Return :
        ---------
        int
            The "pick suggestion score" of the station
        """
        b = 0.33  # coef of dispo in the suggestion score#
        c = 0.33  # coef of the shortage score in the suggestion score#
        n0 = 3  # reference constant set at 3 of availability#
        Spick = CalculationService.compute_short_score(self.station)
        nb_bikes = CalculationService.latest_record(self.station).nb_available_bikes
        Dispo = 1 - math.exp(- nb_bikes / n0)
        if nb_bikes == 0:
            return 0
        elif nb_bikes == 1 and Spick <= 75:
            return 0
        return 100 * round(Dispo ** b * Spick ** c, 2)

    @log
    def station_drop_suggestion_score(self) -> int:
        """Compute the "drop suggestion score" of the station the user selected

        We assume in this score than the user is located on the station, indeed the distance score values is 1 indeed dont need to appear in the formula

        Return :
        ---------
        int
            The "drop suggestion score" of the station
        """
        b = 0.33  # coef of dispo in the suggestion score#
        c = 0.33  # coef of the saturation score in the suggestion score#
        n0 = 3  # reference constant set at 3 of availability#
        Sdrop = CalculationService.compute_short_score(self.station)
        nb_spot = CalculationService.latest_record(self.station).nb_available_spaces
        Dispo = 1 - math.exp(- nb_spot / n0)
        if nb_spot == 0:
            return 0
        elif nb_spot == 1 and Sdrop <= 75:
            return 0
        return 100 * round(Dispo ** b * Sdrop ** c, 2)

    @log
    def is_recommended_pick(self) -> bool:
        """Tell based on pick suggestion score of the choosen station if we recommend it or not

        Return :
        --------
        bool
            True if the pick suggestion score is high enough, False if not
        """
        if self.station_pick_suggestion_score <= 50:
            return False
        return True

    @log
    def is_recommended_drop(self) -> bool:
        """Tell based on drop suggestion score of the choosen station if we recommend it or not

        Return :
        --------
        bool
            True if the drop suggestion score is high enough, False if not
        """
        if self.station_drop_suggestion_score <= 50:
            return False
        return True

    @log
    def compute_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> int:
        """Compute the distance in meters between two points having their coordonates

        Parameters :
        ------------
        lat1: float
            the latitude of the first point
        lon1: float
            the longitude of the first point
        lat2: float
            the latitude of the second point
        lon2: float
            the longitude of the second point

        Returns :
        ---------
        int
            The distance in meters between the two points
        """
        R = 6371000  # rayon moyen de la terre en mètres#
        a, b = math.radians(lat1), math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        alpha = math.sin(dlat / 2) ** 2 + math.cos(a) * math.cos(b) * math.sin(dlon / 2) ** 2
        return round(2 * R * math.asin(math.sqrt(alpha)))

    @log
    def get_suggestion_pick(self) -> list(Station, int):
        """Select the suggested stations around

        Select all the stations in a close area around the choosen station and with at least 2 available bikes which  have a  pick suggestion score over 50 or at least better than the pick suggestion score than the one of the station choosen by the user (station_pick_suggestion_score)

        Return :
        --------
        list(Station, int)
            The list of the recommended stations with their score
        """
        a = 0.33
        b = 0.33
        c = 0.34
        n0 = 3
        station_sugg = {}
        for stations in StationService.list_all():
            dist = self.compute_distance(self.station.lat, self.station.lon, stations.lat, stations.lon)
            nb_bikes = CalculationService.latest_record(stations).nb_available_bikes
            if dist <= 1000 and nb_bikes >= 2:  # 1000 is arbitrary#
                Spick = CalculationService.compute_short_score(self.stations)
                d = 1 - math.exp(- dist / 800)  # 800 is arbitrary#
                Disp = 1 - math.exp(- nb_bikes / n0)
                sugg_score = d ** a * Disp ** b * Spick ** c
                if sugg_score >= 50 or sugg_score >= self.station_pick_suggestion_score:  # 50 is arbitrary#
                    station_sugg[stations] = sugg_score
        sugg = sorted(sugg_score.items(), key=lambda x: x[1], reverse=True)
        return sugg

    @log
    def get_suggestion_drop(self) -> list(Station, int):
        """Select the suggested stations around

        Select all the stations in a close area around the choosen station and with at least 2 available spots which  have a  drop suggestion score over 50 or at least better than the drop suggestion score than the one of the station choosen by the user (station_drop_suggestion_score)

        Return :
        --------
        list(Station, int)
            The list of the recommended stations and their score
        """
        a = 0.33
        b = 0.33
        c = 0.34
        n0 = 3
        station_sugg = {}
        for stations in StationService.list_all():
            dist = self.compute_distance(self.station.lat, self.station.lon, stations.lat, stations.lon)
            nb_spot = CalculationService.latest_record(stations).nb_available_spaces
            if dist <= 1000 and nb_spot >= 2:  # 1000 is arbitrary#
                Sdrop = CalculationService.compute_sat_score(self.stations)
                d = 1 - math.exp(- dist / 800)  # 800 is arbitrary#
                Disp = 1 - math.exp(- nb_spot / n0)
                sugg_score = d ** a * Disp ** b * Sdrop ** c
                if sugg_score >= 50 or sugg_score >= self.station_drop_suggestion_score:  # 50 is arbitrary#
                    station_sugg[stations] = sugg_score
        sugg = sorted(sugg_score.items(), key=lambda x: x[1], reverse=True)
        return sugg
