from unittest.mock import MagicMock

from dao.user_dao import UserDao
from service.user_service import UserService


def test_create_ok():
    """Tests the successful creation of a user"""
    UserDao().create = MagicMock(return_value=True)
    user = UserService().create(username="Jean", pwd="123")
    assert user.username == "Jean"
