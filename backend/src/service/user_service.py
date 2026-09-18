from business_object.user import User
from dao.user_dao import UserDao


class UserService:

    def create(self, pseudo: str, pwdh: str):
        new_user = User(pseudo=pseudo, pwdh=pwdh)
        return new_user if UserDao().create(new_user) else None
