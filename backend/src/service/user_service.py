from business_object.user import User
from dao.user_dao import UserDao
from utils.log_utils import log
from utils.security import hash_password
import secrets


class UserService:

    @log
    def create(self, username: str, pwd: str) -> User:
        """Asks to create a new user in the system
        Parameters
        ----------
        username : str
            username of the new user
        pwd : str
            password, will be hashed before storage
        Returns
        -------
            User object created or None if creation failed.
        """
        new_user = User(
            username=username,
            pwdh=hash_password(pwd, username)
        )
        return new_user if UserDao().create(new_user) else None

    @log
    def list_all(self) -> list[User]:
        """Retrieves all users from the database by asking to the dao
        Returns
        --------
            list[User]
        """
        return UserDao().list_all()

    @log
    def login(self, username: str, pwd: str) -> User:
        """Asks to authenticate a player using their credentials
        Parameters
        ----------
        username : str
            username of the new user
        pwd : str
            password, will be hashed
        Returns
        -------
            User object if authentication is successful, otherwise None
        """
        user = User().login(username, hash_password(pwd, username))
        if user:
            # Generate a token and update the Player
            user.access_token = secrets.token_urlsafe(32)
            self.update(user)
            return user
        return None
