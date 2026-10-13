from fastapi import APIRouter, Depends, HTTPException

from schema.station_model import FavoriteAddModel
from service.station_service import FavoriteService
from utils.log_utils import get_logger

router = APIRouter()

logger = get_logger(__name__)


def get_favorite_service():
    """Dependency Injection provider for FavoriteService."""
    return FavoriteService()


@router.post("/", response_model=FavoriteAddModel, tags=["Favorites"])
async def add_favorite(favorite: FavoriteAddModel, favorite_service=Depends(get_favorite_service)):
    """Add a new favorite to the database.
    Parameters
    ----------
    favorite : FavoriteAddModel
        The favorite to add.
    station_service : StationService
        The service used to interact with station data
    Returns
    -------
        FavoriteAddModel: The newly added favorite data.
    Raises:
        HTTPException: 400 error if the favorite already exists.
        HTTPException: 500 error if the creation process fails.
    """
    logger.info("Add a favorite")
    if favorite_service.favorite_already_exists(favorite):
        raise HTTPException(status_code=400, detail="Favorite already exists.")
    favorite = favorite_service.add_favorite(favorite)
    if not favorite:
        raise HTTPException(status_code=500, detail="Error while adding favorite.")
    return favorite


# à retravailler : quel argument ? quelles vérifications ? Similaire à delete un joueur ?
@router.delete("/{id_user}", tags=["Favorites"])
async def delete_favorite(station_service=Depends(get_favorite_service)):
    """Delete a favorite from the database."""
    pass
