from business_object.user import User
from dao.db_connection import DBConnection
from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)


class UserDao(metaclass=Singleton):
    @log
    def create(self, user: User) -> bool:
        """Create a user in the database
        Parameters
        ----------
        user:User
            user who should be created
        Returns
        -------
        bool
            True if the user is created in the database, false else
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO project.Users(username, pwdh) VALUES "
                        "(%(username)s, %(pwdh)s) "
                        "RETURNING id_user;",
                        {"username": user.username, "pwdh": user.pwdh},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        created = False
        if res:
            user.id_user = int(res["id_user"])
            created = True
        return created

    @log
    def list_all(self) -> list[User]:
        """List all users found in the database
        Returns
        -------
        list[User]
            list of all the users
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id_user, username, pwdh, admin FROM project.Users")
                    res = cursor.fetchall()
        except Exception as e:
            logger.error(e)
            raise

        users_list = []
        if res:
            for row in res:
                user = User(
                    id_user=row["id_user"],
                    username=row["username"],
                    pwdh=row["pwdh"],
                    admin=row["admin"],
                )
                users_list.append(user)
        return users_list

    @log
    def login(self, username: str, pwdh: str) -> User:
        """Verify the match between given variables and database variables
        Parameters
        ----------
        username: str
            username of the user
        pwdh: str
            hashed password
        Returns
        -------
        User:
            user associated if the username and password match
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_user, username, pwdh, admin "
                        "FROM project.Users "
                        "WHERE username = %(username)s AND pwdh = %(pwdh)s",
                        {"username": username, "pwdh": pwdh},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise
        user = None
        if res:
            user = User(
                id_user=res["id_user"],
                username=res["username"],
                pwdh=res["pwdh"],
                admin=res["admin"],
            )
        return user

    @log
    def update(self, user: User) -> bool:
        """Update a user in the database.
        Parameters
        ----------
        user: User
            user to be updated
        Returns
        -------
            True if update is successful, False otherwise
        """
        nb_affected_rows = 0

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE project.Users                                           "
                        "   SET username = %(username)s,                                "
                        "       id_user = COALESCE(%(id_user)s, id_user), "
                        "       admin = COALESCE(%(admin)s, admin), "
                        "       pwdh = COALESCE(%(pwdh)s, pwdh),            "
                        "       access_token = COALESCE(%(access_token)s, access_token) "
                        " WHERE id_user = %(id_user)s;                              ",
                        {
                            "username": user.username,
                            "id_user": user.id_user,
                            "admin": user.admin,
                            "pwdh": user.pwdh,
                            "access_token": user.access_token,
                        },
                    )
                    nb_affected_rows = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return nb_affected_rows == 1

    @log
    def find_by_id(self, id_user: int) -> User:
        """Find a user by their id.
        Args:
            id_user (int): The ID of the user to find
        Returns:
            User matching the given id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                            "
                        "  FROM users                       "
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
                pwdh=res["pwdh"]
            )

        return user

    @log
    def delete(self, user) -> bool:
        """Delete a user from the database.
        Args:
            User to delete from the database
        Returns:
            True if the user was successfully deleted, False otherwise
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM users                               "
                        " WHERE id_user = %(id_user)s                 ",
                        {"id_user": user.id_user},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logger.error(e)
            raise

        return res > 0

    @log
    def find_by_token(self, access_token: str) -> User:
        """Find a user by their access token.
        Args:
            access_token (str): The token to search for.
        Returns:
            User object if found, otherwise None.
        """
        if not access_token:
            return None

        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                                "
                        "  FROM users                           "
                        " WHERE access_token = %(token)s;        ",
                        {"token": access_token},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(f"Error finding user by token: {e}")
            raise

        user = None
        if res:
            user = User(
                id_user=res["id_user"],
                username=res["username"],
                pwdh=res["pwdh"],
                admin=res["admin"],
            )

        return user
