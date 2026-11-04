from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch
from business_object.station import Station
from business_object.station_record import StationRecord
from service.suggestion_service import SuggestionService
from service.calculation_service import CalculationService
from service.station_service import StationService
import pytest

TZ = timezone(timedelta(hours=2))  # +02


def d(heure: str) -> datetime:
    """Constructs a value in datetime format for 2026-10-13 at the specified time (time zone +02)"""
    return datetime.fromisoformat(f"2026-10-13 {heure}:00").replace(tzinfo=TZ)


# Table Stations
stations = [
    Station(5501, "République", 48.110026, -1.678037, 45),
    Station(5502, "Mairie-Opéra", 48.111624, -1.678757, 24),
    Station(5504, "Place Hoche", 48.115074, -1.677073, 39),
    Station(5505, "Sainte-Anne", 48.114219, -1.680534, 24),
    Station(5509, "Saint-Georges Piscine", 48.112385, -1.674417, 18),
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


def test_station_pick_suggestion_score():
    with patch.object(CalculationService, "compute_short_score", return_value=1.0):
        assert suggestion_service_rep.station_pick_suggestion_score() == 100
    with patch.object(CalculationService, "compute_short_score", return_value=0.43):
        assert suggestion_service_mai.station_pick_suggestion_score() == 81
    with patch.object(CalculationService, "compute_short_score", return_value=1.0):
        assert suggestion_service_pla.station_pick_suggestion_score() == 80
    with patch.object(CalculationService, "compute_short_score", return_value=1.0):
        assert suggestion_service_sai.station_pick_suggestion_score() == 0
    with patch.object(CalculationService, "compute_short_score", return_value=0.48):
        assert suggestion_service_pis.station_pick_suggestion_score() == 0


def test_station_drop_suggestion_score():
    with patch.object(CalculationService, "compute_sat_score", return_value=0.33):
        assert suggestion_service_rep.station_drop_suggestion_score() == 0
    with patch.object(CalculationService, "compute_sat_score", return_value=1.0):
        assert suggestion_service_mai.station_drop_suggestion_score() == 94
    with patch.object(CalculationService, "compute_sat_score", return_value=1.0):
        assert suggestion_service_pla.station_drop_suggestion_score() == 100
    with patch.object(CalculationService, "compute_sat_score", return_value=0.0):
        assert suggestion_service_sai.station_drop_suggestion_score() == 0
    with patch.object(CalculationService, "compute_sat_score", return_value=0.51):
        assert suggestion_service_pis.station_drop_suggestion_score() == 86


suggestion_service_rep.station_pick_suggestion_score = MagicMock(return_value=100)
suggestion_service_mai.station_pick_suggestion_score = MagicMock(return_value=81)
suggestion_service_pla.station_pick_suggestion_score = MagicMock(return_value=80)
suggestion_service_sai.station_pick_suggestion_score = MagicMock(return_value=0)
suggestion_service_pis.station_pick_suggestion_score = MagicMock(return_value=0)

suggestion_service_rep.station_drop_suggestion_score = MagicMock(return_value=0)
suggestion_service_mai.station_drop_suggestion_score = MagicMock(return_value=94)
suggestion_service_pla.station_drop_suggestion_score = MagicMock(return_value=100)
suggestion_service_sai.station_drop_suggestion_score = MagicMock(return_value=0)
suggestion_service_pis.station_drop_suggestion_score = MagicMock(return_value=86)


def test_is_recommended_pick():
    assert suggestion_service_rep.is_recommended_pick() is True
    assert suggestion_service_mai.is_recommended_pick() is True
    assert suggestion_service_pla.is_recommended_pick() is True
    assert suggestion_service_sai.is_recommended_pick() is False
    assert suggestion_service_pis.is_recommended_pick() is False


def test_is_recommended_drop():
    assert suggestion_service_rep.is_recommended_drop() is False
    assert suggestion_service_mai.is_recommended_drop() is True
    assert suggestion_service_pla.is_recommended_drop() is True
    assert suggestion_service_sai.is_recommended_drop() is False
    assert suggestion_service_pis.is_recommended_drop() is True


def test_compute_distance():
    assert suggestion_service_mai.compute_distance(
        48.110026,
        -1.678037,
        48.111624,
        -1.678757
        ) == 186
    assert suggestion_service_mai.compute_distance(
        48.115074,
        -1.677073,
        48.114219,
        -1.680534
        ) == 274
