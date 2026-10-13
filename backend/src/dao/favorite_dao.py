from business_object.favorite import Favorite
from dao.db_connection import DBConnection
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class FavoriteDao(metaclass=Singleton):
    @log
    def add_favorite(self, favorite: Favorite) -> bool:
        """Create a favorite in the database
        Parameters
        ----------
        favorite:Favorite
            favorite to add
        Returns
        -------
        bool
            True if the favorite is added in the database, otherwise false
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO project.Favorites(id_user, id_station) VALUES "
                        "(%(id_user)s, %(id_station)s) "
                        "RETURNING *; ",
                        {"id_user": favorite.id_user, "id_station": favorite.id_station},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        added = False
        if res:
            added = True
        return added

    @log
    def list_all(self) -> list[Favorite]:
        """List all favorites found in the database
        Returns
        -------
        list[Favorite]
            list of all the favorites
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM project.Favorites")
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        favorites_list = []
        if res:
            for row in res:
                station = Favorite(id_user=row["id_user"], id_station=row["id_station"])
                favorites_list.append(station)
        return favorites_list
