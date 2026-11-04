from datetime import datetime, timedelta, timezone

from business_object.station import Station
from business_object.station_record import StationRecord
from service.calculation_service import CalculationService

TZ = timezone(timedelta(hours=2))  # +02

# Table Stations
stations = [
    Station(5501, "République", 48.110026, -1.678037, 45),
    Station(5502, "Mairie-Opéra", 48.111624, -1.678757, 24),
    Station(5504, "Place Hoche", 48.115074, -1.677073, 39),
    Station(5505, "Sainte-Anne", 48.114219, -1.680534, 24),
    Station(5509, "Saint-Georges Piscine", 48.112385, -1.674417, 18),
]


def d(heure: str) -> datetime:
    """Constructs a value in datetime format for 2026-10-13 at the specified time (time zone +02)."""
    return datetime.fromisoformat(f"2026-10-13 {heure}:00").replace(tzinfo=TZ)


# Table StationRecords
station_records = [
    # Station 5501
    StationRecord(5501, d("08:00"), "IN_SERVICE", 25, 20, 10),
    StationRecord(5501, d("08:15"), "IN_SERVICE", 20, 25, 10),
    StationRecord(5501, d("08:30"), "IN_SERVICE", 10, 35, 10),
    StationRecord(5501, d("08:45"), "IN_SERVICE", 0, 45, 10),
    StationRecord(5501, d("09:00"), "IN_SERVICE", 0, 45, 10),
    StationRecord(5501, d("09:15"), "IN_SERVICE", 0, 45, 10),
    StationRecord(5501, d("09:30"), "IN_SERVICE", 0, 45, 10),
    StationRecord(5501, d("09:45"), "IN_SERVICE", 0, 45, 10),
    StationRecord(5501, d("10:00"), "IN_SERVICE", 0, 45, 10),
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
    StationRecord(5504, d("08:00"), "IN_SERVICE", 13, 26, 13),
    StationRecord(5504, d("08:15"), "IN_SERVICE", 15, 24, 10),
    StationRecord(5504, d("08:30"), "IN_SERVICE", 21, 18, 10),
    StationRecord(5504, d("08:45"), "IN_SERVICE", 32, 7, 7),
    StationRecord(5504, d("09:00"), "IN_SERVICE", 34, 5, 5),
    StationRecord(5504, d("09:15"), "IN_SERVICE", 36, 3, 3),
    StationRecord(5504, d("09:30"), "IN_SERVICE", 33, 6, 3),
    StationRecord(5504, d("09:45"), "IN_SERVICE", 31, 8, 3),
    StationRecord(5504, d("10:00"), "IN_SERVICE", 31, 8, 3),
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
    # Station 5509
    StationRecord(5509, d("08:00"), "IN_SERVICE", 18, 0, 0),
    StationRecord(5509, d("08:15"), "IN_SERVICE", 18, 0, 0),
    StationRecord(5509, d("08:30"), "IN_SERVICE", 18, 0, 0),
    StationRecord(5509, d("08:45"), "IN_SERVICE", 0, 18, 3),
    StationRecord(5509, d("09:00"), "IN_SERVICE", 0, 18, 3),
    StationRecord(5509, d("09:15"), "IN_SERVICE", 0, 18, 3),
    StationRecord(5509, d("09:30"), "IN_SERVICE", 0, 18, 0),
    StationRecord(5509, d("09:45"), "IN_SERVICE", 18, 0, 0),
    StationRecord(5509, d("10:00"), "IN_SERVICE", 18, 0, 0),
    StationRecord(5509, d("10:15"), "IN_SERVICE", 18, 0, 0),
    StationRecord(5509, d("10:30"), "IN_SERVICE", 18, 0, 0),
    StationRecord(5509, d("10:45"), "IN_SERVICE", 0, 18, 0),
    StationRecord(5509, d("11:00"), "IN_SERVICE", 0, 18, 3),
    StationRecord(5509, d("11:15"), "IN_SERVICE", 0, 18, 3),
    StationRecord(5509, d("11:30"), "IN_SERVICE", 12, 3, 3),
    StationRecord(5509, d("11:45"), "IN_SERVICE", 0, 18, 3),
    StationRecord(5509, d("12:00"), "IN_SERVICE", 0, 18, 3),
]

calculation_service_rep = CalculationService(station=stations[0])
calculation_service_rep.station_records = station_records[0:9]
calculation_service_mai = CalculationService(station=stations[1])
calculation_service_mai.station_records = station_records[9:18]
calculation_service_pla = CalculationService(station=stations[2])
calculation_service_pla.station_records = station_records[18:27]
calculation_service_sai = CalculationService(station=stations[3])
calculation_service_sai.station_records = station_records[27:36]
calculation_service_pis = CalculationService(station=stations[4])
calculation_service_pis.station_records = station_records[36:53]


def test_latest_record():
    assert calculation_service_rep.latest_record() == calculation_service_rep.station_records[8]


def test_compute_fill_rate():
    assert calculation_service_rep.compute_fill_rate() == 1.0
    assert round(calculation_service_mai.compute_fill_rate(), 2) == 0.54
    assert round(calculation_service_pla.compute_fill_rate(), 2) == 0.21
    assert calculation_service_sai.compute_fill_rate() == 0.0


def test_compute_shortage_rate():
    assert calculation_service_rep.compute_shortage_rate() == 0.0
    assert calculation_service_mai.compute_shortage_rate() == 0.5
    assert calculation_service_pla.compute_shortage_rate() == 0.0
    assert calculation_service_sai.compute_shortage_rate() == 0.0
    assert calculation_service_pis.compute_shortage_rate() == 0.4375


def test_compute_shortage_mean_time():
    assert calculation_service_rep.compute_shortage_mean_time() == 0.0
    assert calculation_service_mai.compute_shortage_mean_time() == 3600
    assert calculation_service_pla.compute_shortage_mean_time() == 0.0
    assert calculation_service_sai.compute_shortage_mean_time() == 0.0
    assert calculation_service_pis.compute_shortage_mean_time() == 3150.0


def test_compute_short_score():
    assert calculation_service_rep.compute_short_score() == 1.0
    assert calculation_service_mai.compute_short_score() == 0.43
    assert calculation_service_pla.compute_short_score() == 1.0
    assert calculation_service_sai.compute_short_score() == 1.0
    assert calculation_service_pis.compute_short_score() == 0.48


def test_compute_saturation_rate():
    assert calculation_service_rep.compute_saturation_rate() == 0.625
    assert calculation_service_mai.compute_saturation_rate() == 0.0
    assert calculation_service_pla.compute_saturation_rate() == 0.0
    assert calculation_service_sai.compute_saturation_rate() == 1.00
    assert calculation_service_pis.compute_saturation_rate() == 0.5


def test_compute_saturation_mean_time():
    assert calculation_service_rep.compute_saturation_mean_time() == 4500.0
    assert calculation_service_mai.compute_saturation_mean_time() == 0.0
    assert calculation_service_pla.compute_saturation_mean_time() == 0.0
    assert calculation_service_sai.compute_saturation_mean_time() == 7200.0
    assert calculation_service_pis.compute_saturation_mean_time() == 2400.0


def test_compute_sat_score():
    assert calculation_service_rep.compute_sat_score() == 0.33
    assert calculation_service_mai.compute_sat_score() == 1.0
    assert calculation_service_pla.compute_sat_score() == 1.0
    assert calculation_service_sai.compute_sat_score() == 0.0
    assert calculation_service_pis.compute_sat_score() == 0.51


def test_compute_score():
    assert calculation_service_rep.compute_score() == 66
    assert calculation_service_mai.compute_score() == 72
    assert calculation_service_pla.compute_score() == 100
    assert calculation_service_sai.compute_score() == 50
    assert calculation_service_pis.compute_score() == 50
