from unittest.mock import MagicMock

from business_object.station import Station
from dao.station_dao import StationDao
from service.station_service import StationService

station = Station("5501", "République", 48.110026, -1.678037, 45)

stations = [
    Station("5501", "République", 48.110026, -1.678037, 45),
    Station("5502", "Mairie-Opéra", 48.111624, -1.678757, 24),
    Station("5504", "Place Hoche", 48.115074, -1.677073, 39),
    Station("5505", "Sainte-Anne", 48.114219, -1.680534, 24),
    Station("5509", "Saint-Georges Piscine", 48.112385, -1.674417, 18),
]


def test_find_by_id():
    """Test for finding a station by its id"""
    StationDao().find_by_id = MagicMock(
        return_value=Station("5501", "République", 48.110026, -1.678037, 45)
    )
    response = StationService().find_by_id("5501")
    assert response.id_station == "5501"


def test_list_all():
    """Test for finding the list of all stations"""
    StationDao().list_all = MagicMock(return_value=stations)
    response = StationService().list_all()
    assert len(response) == 5
    assert stations[0].id_station == "5501"
