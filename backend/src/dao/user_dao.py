from dao.db_connection import DBConnection
from utils.singleton import Singleton
from dotenv import load_dotenv
load_dotenv()

class UserDao(metaclass=Singleton):

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
            print(f"Erreur DAO create: {e}", flush=True)

        created = False
        if res:
            user.id_player = res["id_user"]
            created = True
        return created


