from fastapi import APIRouter, Depends, HTTPException

from schema.station_model import (
    StationDataModel,
    StationLatestRecordModel,
    StationReadModel,
    StationSuggestionModel,
)
from service.calculation_service import CalculationService
from service.station_service import StationService
from service.suggestion_service import SuggestionService
from utils.log_utils import get_logger

router = APIRouter()

logger = get_logger(__name__)


def get_station_service():
    """Dependency Injection provider for StationService."""
    return StationService()


@router.get("/", response_model=list[StationReadModel], tags=["Stations"])
async def list_all_stations(station_service=Depends(get_station_service)):
    """List all stations.
    Returns:
        list[StationReadModel]: A list of all registered stations.
    """
    logger.info("List all stations")
    stations_list = station_service.list_all()
    return stations_list


@router.get("/{id_station}", response_model=StationDataModel, tags=["Stations"])
async def station_by_id(id_station: str, range: int, station_service=Depends(get_station_service)):
    """Find a station by its unique ID.
    Parameters
    ----------
    id_station: str
        The ID of the station
    range: int
        Range of time for the availibility
    station_service : StationService
        The service used to interact with station data
    Returns
    -------
    StationReadModel
        The station data if found
    Raises:
        HTTPException: 404 error if the station is not found
    """
    logger.info("Find a station by id")
    station = station_service.find_by_id(id_station)
    if not station:
        raise HTTPException(status_code=404, detail=f"Station (id={id_station}) not found.")
    stats = station_service.get_stats(station)
    status = CalculationService(station).latest_record().status
    availability_spaces = CalculationService(station).get_availability_spaces_over_time(range)
    availability_bikes = CalculationService(station).get_availability_bikes_over_time(range)
    prediction_spaces = CalculationService(station).prediction_spaces_in_an_hour()
    prediction_bikes = CalculationService(station).prediction_bikes_in_an_hour()
    data = {
        "id_station": station.id_station,
        "name": station.name,
        "lat": station.lat,
        "lon": station.lon,
        "capacity": station.capacity,
        "status": status,
    }
    score = CalculationService(station).compute_score()
    return (
        data
        | stats
        | {"score": score}
        | {"availability_spaces": availability_spaces}
        | {"availability_bikes": availability_bikes}
        | {"prediction_spaces": prediction_spaces}
        | {"prediction_bikes": prediction_bikes}
    )


@router.get(
    "/suggestions/{id_station}", response_model=list[StationSuggestionModel], tags=["Stations"]
)
async def suggestions(
    id_station: str, choice_bool: bool, station_service=Depends(get_station_service)
):
    station = station_service.find_by_id(id_station)
    if choice_bool is True:
        suggestions = SuggestionService(station).get_suggestion_pick()
    else:
        suggestions = SuggestionService(station).get_suggestion_drop()
    return [
        {
            "station": {
                "id_station": station_sugg.id_station,
                "name": station_sugg.name,
                "lat": station_sugg.lat,
                "lon": station_sugg.lon,
                "capacity": station_sugg.capacity,
            },
            "score": score,
        }
        for station_sugg, score in suggestions
    ]


@router.get("/{id_station}/latest", response_model=StationLatestRecordModel, tags=["Stations"])
async def latest_record(id_station: str, station_service=Depends(get_station_service)):
    """Find the latest record of a station by its unique ID.
    Parameters
    ----------
    id_station: str
        The ID of the station
    Returns
    -------
    StationReadModel
        The latest record station data if found
    Raises:
        HTTPException: 404 error if the station is not found
    """
    logger.info("Find a station by id")
    station = station_service.find_by_id(id_station)
    if not station:
        raise HTTPException(status_code=404, detail=f"Station (id={id_station}) not found.")
    latest_record = CalculationService(station).latest_record()
    return {
        "status": latest_record.status,
        "nb_available_spaces": latest_record.nb_available_spaces,
        "nb_available_bikes": latest_record.nb_available_bikes,
    }
