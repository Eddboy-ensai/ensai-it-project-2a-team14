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

    @log
    def delete(self, favorite) -> bool:
        """Delete a favorite from the database.
        Parameters
        ----------
            Favorite to delete from the database
        Returns
        -------
            True if the favorite was successfully deleted, False otherwise
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM project.Favorites                               "
                        " WHERE id_user = %(id_user)s AND id_station = %(id_station)s ",
                        {"id_user": favorite.id_user, "id_station": favorite.id_station},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise
        return res > 0

    @log
    def find_by_id(self, id_user: int) -> list[Favorite]:
        """Find the favorite of a user by its id.
        Parameter
        ---------
        id_user : int
            The ID of the user
        Return
        ------
            User matching the given id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                            "
                        "  FROM Users                       "
                        " WHERE id_user = %(id_user)s;   ",
                        {"id_user": id_user},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        user = None
        if res:
            user = User(
                username=res["username"],
                id_user=res["id_user"],
                admin=res["admin"],
                pwdh=res["pwdh"],
            )

        return user
