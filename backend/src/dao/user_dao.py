from dao.db_connection import DBConnection
from utils.singleton import Singleton
from utils.log_utils import get_logger, log

logger = get_logger(__name__)


class UserDao(metaclass=Singleton):

    @log
    def create(self, user) -> bool:
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
            print("ERREUR SQL :", repr(e))
            raise

        created = False
        if res:
            user.id_player = res["id_user"]
            created = True
        return created


