from business_object.favorite import Favorite
from dao.favorite_dao import FavoriteDao
from utils.log_utils import log


class FavoriteService:
    @log
    def favorite_already_exists(self, favorite: Favorite) -> bool:
        """Check if a favorite already exists in the databse.
        Parameters
        ----------
        favorite : Favorite
            favorite to check
        Returns
        -------
        bool
            True if the favorite already exists in the database.
        """
        favorites = FavoriteDao().list_all()
        for fav in favorites:
            if fav.id_user == favorite.id_user and fav.id_station == favorite.id_station:
                return True
        return False

    @log
    def add_favorite(self, favorite: Favorite) -> Favorite | None:
        """Call the DAO method to add a favorite.
        Parameters
        ----------
        favorite: Favorite
            the favorite (user/station) to add
        Returns
        -------
        Favorite
            Favorite object created or None if creation failed.
        """
        created = FavoriteDao().add_favorite(favorite)
        if created:
            return favorite
        return None

    @log
    def delete_favorite(self, favorite: Favorite) -> bool:
        """Delete a favorite.
        Parameters
            Favorite object to be deleted.
        Returns
        -------
        bool
            True if deletion was successful, False otherwise.
        """
        return FavoriteDao().delete(favorite)
