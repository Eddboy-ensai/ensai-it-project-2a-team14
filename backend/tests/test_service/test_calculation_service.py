from datetime import datetime, timedelta, timezone

from business_object.station import Station
from business_object.station_record import StationRecord
from service.calculation_service import CalculationService

TZ = timezone(timedelta(hours=2))  # +02

# Table Stations
stations = [
    Station(5501, "République", -1.678037, 48.110026, 45),
    Station(5502, "Mairie-Opéra", -1.678757, 48.111624, 24),
    Station(5504, "Place Hoche", -1.677073, 48.115074, 39),
    Station(5505, "Sainte-Anne", -1.680534, 48.114219, 24),
]


def d(heure: str) -> datetime:
    """Construit un datetime du 2026-10-13 à l'heure donnée (fuseau +02)."""
    return datetime.fromisoformat(f"2026-10-13 {heure}:00").replace(tzinfo=TZ)


# Table StationRecords
station_records = [
    # Station 5501
    StationRecord(5501, d("08:00"), "IN_SERVICE", 25, 10, 10),
    StationRecord(5501, d("08:15"), "IN_SERVICE", 20, 15, 10),
    StationRecord(5501, d("08:30"), "IN_SERVICE", 10, 25, 10),
    StationRecord(5501, d("08:45"), "IN_SERVICE", 0, 35, 10),
    StationRecord(5501, d("09:00"), "IN_SERVICE", 0, 35, 10),
    StationRecord(5501, d("09:15"), "IN_SERVICE", 0, 35, 10),
    StationRecord(5501, d("09:30"), "IN_SERVICE", 0, 35, 10),
    StationRecord(5501, d("09:45"), "IN_SERVICE", 0, 35, 10),
    StationRecord(5501, d("10:00"), "IN_SERVICE", 0, 35, 10),
    # Station 5502
    StationRecord(5502, d("08:00"), "IN_SERVICE", 24, 0, 0),
    StationRecord(5502, d("08:15"), "IN_SERVICE", 24, 0, 0),
    StationRecord(5502, d("08:30"), "IN_SERVICE", 24, 0, 0),
    StationRecord(5502, d("08:45"), "IN_SERVICE", 24, 0, 0),
    StationRecord(5502, d("09:00"), "IN_SERVICE", 19, 5, 0),
    StationRecord(5502, d("09:15"), "IN_SERVICE", 13, 11, 0),
    StationRecord(5502, d("09:30"), "IN_SERVICE", 9, 15, 0),
    StationRecord(5502, d("09:45"), "IN_SERVICE", 11, 13, 0),
    StationRecord(5502, d("10:00"), "IN_SERVICE", 11, 13, 0),
    # Station 5504
    StationRecord(5504, d("08:00"), "IN_SERVICE", 13, 13, 13),
    StationRecord(5504, d("08:15"), "IN_SERVICE", 15, 14, 10),
    StationRecord(5504, d("08:30"), "IN_SERVICE", 21, 8, 10),
    StationRecord(5504, d("08:45"), "IN_SERVICE", 32, 0, 7),
    StationRecord(5504, d("09:00"), "IN_SERVICE", 34, 0, 5),
    StationRecord(5504, d("09:15"), "IN_SERVICE", 36, 0, 3),
    StationRecord(5504, d("09:30"), "IN_SERVICE", 33, 3, 3),
    StationRecord(5504, d("09:45"), "IN_SERVICE", 31, 5, 3),
    StationRecord(5504, d("10:00"), "IN_SERVICE", 31, 5, 3),
    # Station 5505
    StationRecord(5505, d("08:00"), "NOT_INSTALLED", 0, 0, 0),
    StationRecord(5505, d("08:15"), "NOT_INSTALLED", 0, 0, 0),
    StationRecord(5505, d("08:30"), "NOT_INSTALLED", 0, 0, 0),
    StationRecord(5505, d("08:45"), "NOT_INSTALLED", 0, 0, 0),
    StationRecord(5505, d("09:00"), "NOT_INSTALLED", 0, 0, 0),
    StationRecord(5505, d("09:15"), "NOT_INSTALLED", 0, 0, 0),
    StationRecord(5505, d("09:30"), "NOT_INSTALLED", 0, 0, 0),
    StationRecord(5505, d("09:45"), "NOT_INSTALLED", 0, 0, 0),
    StationRecord(5505, d("10:00"), "NOT_INSTALLED", 0, 0, 0),
]

def test_latest_record():
    calculation_service_rep = CalculationService(station=stations[0])
    calculation_service_rep.station_records = station_records[0:9]
    assert calculation_service_rep.latest_record() == calculation_service_rep.station_records[8]

def test_compute_fill_rate():
    calculation_service_rep = CalculationService(station=stations[0])
    calculation_service_rep.station_records = station_records[0:9]
    assert calculation_service_rep.compute_fill_rate() == 1.0
