from fastapi import APIRouter, Depends, HTTPException

from schema.station_model import StationReadModel
from service.user_service import StationService
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


@router.get("/{id_station}", response_model=StationReadModel, tags=["Stations"])
async def station_by_id(id_station: int, station_service=Depends(get_station_service)):
    """Find a station by its unique ID.
    Parameters
    ----------
    id_station: int
        The ID of the station
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
        raise HTTPException(status_code=404, detail=f"User (id={id_station}) not found.")
    return station
