from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

from business_object.station import Station
from business_object.station_record import StationRecord
from service.suggestion_service import SuggestionService
from service.calculation_service import CalculationService

TZ = timezone(timedelta(hours=2))  # +02


def d(heure: str) -> datetime:
    """Constructs a value in datetime format for 2026-10-13 at the specified time (time zone +02)"""
    return datetime.fromisoformat(f"2026-10-13 {heure}:00").replace(tzinfo=TZ)


# Table Stations
stations = [
    Station(5501, "République", -1.678037, 48.110026, 45),
    Station(5502, "Mairie-Opéra", -1.678757, 48.111624, 24),
    Station(5504, "Place Hoche", -1.677073, 48.115074, 39),
    Station(5505, "Sainte-Anne", -1.680534, 48.114219, 24),
    Station(5509, "Saint-Georges Piscine", -1.674417, 48.112385, 18),
]


suggestion_service_rep = SuggestionService(station=stations[0])
suggestion_service_mai = SuggestionService(station=stations[1])
suggestion_service_pla = SuggestionService(station=stations[2])
suggestion_service_sai = SuggestionService(station=stations[3])
suggestion_service_pis = SuggestionService(station=stations[4])


# Table latest_records
latest_records = [
    StationRecord(5501, d("10:00"), "IN_SERVICE", 0, 35, 10),
    StationRecord(5502, d("10:00"), "IN_SERVICE", 11, 13, 0),
    StationRecord(5504, d("10:00"), "IN_SERVICE", 31, 5, 3),
    StationRecord(5505, d("10:00"), "NOT_INSTALLED", 0, 0, 0),
    StationRecord(5509, d("10:00"), "IN_SERVICE", 18, 0, 0),
]

suggestion_service_rep.latest_record = latest_records[0]
suggestion_service_mai.latest_record = latest_records[1]
suggestion_service_pla.latest_record = latest_records[2]
suggestion_service_sai.latest_record = latest_records[3]
suggestion_service_pis.latest_record = latest_records[4]


calculation_service_rep = CalculationService(station=stations[0])
calculation_service_mai = CalculationService(station=stations[1])
calculation_service_pla = CalculationService(station=stations[2])
calculation_service_sai = CalculationService(station=stations[3])
calculation_service_pis = CalculationService(station=stations[4])


calculation_service_rep.compute_sat_score = MagicMock(return_value=0.33)
calculation_service_rep.compute_short_score = MagicMock(return_value=1.0)
calculation_service_mai.compute_sat_score = MagicMock(return_value=1.0)
calculation_service_mai.compute_short_score = MagicMock(return_value=0.43)
calculation_service_pla.compute_sat_score = MagicMock(return_value=1.0)
calculation_service_pla.compute_short_score = MagicMock(return_value=1.0)
calculation_service_sai.compute_sat_score = MagicMock(return_value=0.0)
calculation_service_sai.compute_short_score = MagicMock(return_value=1.0)
calculation_service_pis.compute_sat_score = MagicMock(return_value=0.51)
calculation_service_pis.compute_short_score = MagicMock(return_value=0.48)


def test_station_pick_suggestion_score():
    assert suggestion_service_rep.station_pick_suggestion_score == 100
    assert suggestion_service_mai.station_pick_suggestion_score == 81
    assert suggestion_service_pla.station_pick_suggestion_score == 80
    assert suggestion_service_sai.station_pick_suggestion_score == 0
    assert suggestion_service_pis.station_pick_suggestion_score == 0
