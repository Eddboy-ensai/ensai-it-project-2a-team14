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
                        "INSERT INTO project.Users(pseudo, pwdh) VALUES "
                        "(%(pseudo)s, %(pwdh)s) "
                        "RETURNING id_user;",
                        {
                            "pseudo": user.pseudo,
                            "pwdh": user.pwdh
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        created = False
        if res:
            user.id_player = res["id_user"]
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
                        "SELECT id_user, pseudo, pwdh, admin"
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
                    id_user=row["id_player"],
                    pseudo=row["pseudo"],
                    pwdh=row["pwdh"],
                    admin=row["admin"]
                )
                users_list.append(user)
        return users_list

    @log
    def login(self, pseudo: str, pwdh: str) -> User:
        """Verify the match between given variables and database variables
        Parameters
        ----------
        pseudo: str
            pseudo of the user
        pwdh: str
            hashed password
        Returns
        -------
        User:
            user associated if the pseudo and password match
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_user, pseudo, pwdh, admin"
                        "FROM project.Users"
                        "WHERE pseudo == %(pseudo)s AND pwdh == %(pwdh)s",
                        {"pseudo": pseudo, "pwdh": pwdh}
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise
        user = None
        if res:
            user = User(
                id_user=res["id_player"],
                pseudo=res["pseudo"],
                pwdh=res["pwdh"],
                admin=res["admin"]
            )
        return user
