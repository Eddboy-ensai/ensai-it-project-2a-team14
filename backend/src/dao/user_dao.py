from dao.db_connection import DBConnection
from utils.singleton import Singleton
from utils.log_utils import get_logger, log
from business_object.user import User

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
                        {
                            "username": user.username,
                            "pwdh": user.pwdh
                        },
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
        """ List all users found in the database
        Returns
        -------
        list[User]
            list of all the users
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_user, username, pwdh, admin"
                        "FROM project.Users"
                    )
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
                    admin=row["admin"]
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
                        "SELECT id_user, username, pwdh, admin"
                        "FROM project.Users"
                        "WHERE username = %(username)s AND pwdh = %(pwdh)s",
                        {"username": username, "pwdh": pwdh}
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
                admin=res["admin"]
            )
        return user
