from business_object.user import User
from dao.user_dao import UserDao
from utils.log_utils import log
from utils.security import hash_password
import secrets


class UserService:

    @log
    def create(self, username, password) -> User:
        """Creates a new user in the system.
        Args:
            username (str)
            password (str) will be hashed before storage
        Returns:
            User object created or None if creation failed.
        """
        new_user = User(
            username=username,
            password=hash_password(password, username)
        )
        return new_user if user_dao().create(new_user) else None

    @log
    def list_all(self) -> list[User]:
        """Retrieves all users from the database by asking to the dao
        Returns:
            list[User]
        """
        return user_dao().list_all()

    @log
    def login(self, username: str, password: str) -> User:
        """Authenticates a player using their credentials.
        Args:
            username (str)
            password (str)
        Returns:
            User object if authentication is successful, otherwise None.
        """
        user = user_dao().login(username, hash_password(password, username))
        if user:
            # Generate a token and update the Player
            user.access_token = secrets.token_urlsafe(32)
            self.update(user)
            return user
        return None
