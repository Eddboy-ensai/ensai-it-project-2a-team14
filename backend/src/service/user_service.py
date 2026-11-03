import secrets

from business_object.user import User
from dao.user_dao import UserDao
from utils.log_utils import log
from utils.security import hash_password


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
        new_user = User(username, hash_password(pwd, username))
        created = UserDao().create(new_user)
        if created:
            return new_user
        return None

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
        """Asks to authenticate a user using their credentials
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
        user = UserDao().login(username, hash_password(pwd, username))
        if user:
            # Generate a token and update the User
            user.access_token = secrets.token_urlsafe(32)
            self.update(user)
            return user
        return None

    @log
    def update(self, user: User) -> User:
        """Updates an existing user's information.
        Parameters
        ----------
        user: User
            User object containing updated information
        Returns
        -------
        User : the updated user object, or None if the update failed
        """
        return user if UserDao().update(user) else None

    @log
    def update_own_profile(
        self,
        user: User,
        current_pwd: str,
        new_username: str | None = None,
        new_pwd: str | None = None,
    ) -> User:
        """Updates the profile of the logged-in user (username and/or password).
        Parameters
        ----------
        user : User
            the logged-in user (returned by verify_token)
        current_pwd : str
            current password, checked before any modification
        new_username : str | None
            new username, or None to keep the current one
        new_pwd : str | None
            new password, or None to keep the current one
        Returns
        -------
        User : the updated user, or None if the update failed in the database
        Raises
        ------
        PermissionError : if the current password is wrong
        ValueError : if there is nothing to update or the username is already used
        """
        if hash_password(current_pwd, user.username) != user.pwdh:
            raise PermissionError("Wrong current password.")
        if not new_username and not new_pwd:
            raise ValueError("Nothing to update.")

        username = new_username or user.username
        if username != user.username and self.username_already_used(username):
            raise ValueError("Username already used.")

        # The hash is salted with the username: it must be recomputed
        # even if only the username changes.
        user.username = username
        user.pwdh = hash_password(new_pwd or current_pwd, username)
        return self.update(user)

    @log
    def username_already_used(self, username: str) -> bool:
        """Check if a username is already used.
        Parameters
        ----------
        username : str
            username to check
        Returns
        -------
        bool
            True if the username already exists in the database.
        """
        users = UserDao().list_all()
        return username in [p.username for p in users]

    @log
    def find_by_id(self, id_user: int) -> User:
        """Finds a specific user by their unique id.
        Args:
            id_user (int)
        Returns:
            User object if found, otherwise None.
        """
        return UserDao().find_by_id(id_user)

    @log
    def delete(self, user) -> bool:
        """Delete a user account.
        Args:
            User object to be deleted.
        Returns:
            True if deletion was successful, False otherwise.
        """
        return UserDao().delete(user)
