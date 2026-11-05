from fastapi import APIRouter, Depends, HTTPException

from business_object.favorite import Favorite
from schema.favorite_model import FavoriteAddModel, FavoriteDeleteModel, ListFavoritesModel
from service.favorite_service import FavoriteService
from service.station_service import StationService
from utils.log_utils import get_logger
from utils.security import verify_token

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
async def delete_favorite(
    id_user: int, body: FavoriteDeleteModel, favorite_service=Depends(get_favorite_service)
):
    """Delete a favorite from the database."""
    favorite = Favorite(id_user, body.id_station)
    if not favorite_service.favorite_already_exists(favorite):
        raise HTTPException(status_code=404, detail="Favorite not found.")
    favorite_service.delete_favorite(favorite)
    return "Favori supprimé"


@router.get("/", response_model=ListFavoritesModel, tags=["Favorites"])
async def favorite_by_token(current_user=Depends(verify_token)):
    """Find a user's favorite station by their unique token."""
    logger.info("Find a user by his Token")
    favorites = []
    for fav in FavoriteService().find_by_id(current_user.id_user):
        favorites.append({
            "id_station": fav.id_station,
            "name": StationService().find_by_id(fav.id_station).name,
        })
    return {"favorites": favorites}
