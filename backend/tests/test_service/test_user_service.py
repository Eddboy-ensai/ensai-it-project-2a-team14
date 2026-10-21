from unittest.mock import MagicMock

from business_object.user import User
from dao.user_dao import UserDao
from service.user_service import UserService

users_list = [User("jojo", "123"), User("fafa", "789")]


def test_create_ok():
    """Tests the successful creation of a user"""
    UserDao().create = MagicMock(return_value=True)
    user = UserService().create(username="Jean", pwd="123")
    assert user.username == "Jean"


def test_create_fail():
    """Tests a failed creation of a user"""
    UserDao().create = MagicMock(return_value=False)
    user = UserService().create(username="Jean", pwd="123")
    assert user is None


def test_username_already_used_yes():
    username = "jojo"
    UserDao().list_all = MagicMock(return_value=users_list)
    res = UserService().username_already_used(username)
    assert res


def test_username_already_used_no():
    username = "mimi"
    UserDao().list_all = MagicMock(return_value=users_list)
    res = UserService().username_already_used(username)
    assert not res
