from unittest.mock import MagicMock

from business_object.favorite import Favorite
from dao.favorite_dao import FavoriteDao
from service.favorite_service import FavoriteService

favorite = Favorite(id_user=1, id_station="5501")


def test_add_favorite():
    """Test for adding a favorite station"""
    FavoriteDao().add_favorite = MagicMock(return_value=Favorite(id_user=1, id_station="5501"))
    favorite_added = FavoriteService().add_favorite(favorite)
    assert favorite.id_user == favorite_added.id_user
    assert favorite.id_station == favorite.id_station


def test_add_favorite_None():
    """Test for adding a favorite station (None return)"""
    FavoriteDao().add_favorite = MagicMock(return_value=None)
    response = FavoriteService().add_favorite(favorite)
    assert response is None


def test_delete_favorite_true():
    """Test for deleting a favorite station (case True)"""
    FavoriteDao().delete_favorite = MagicMock(return_value=True)
    response = FavoriteService().delete_favorite(favorite)
    assert response is True


def test_delete_favorite_false():
    """Test for deleting a favorite station (case False)"""
    FavoriteDao().delete_favorite = MagicMock(return_value=False)
    response = FavoriteService().delete_favorite(favorite)
    assert response is False


def test_find_by_id():
    """Test for finding favorites station"""
    FavoriteDao().find_by_id = MagicMock(return_value=[Favorite(id_user=1, id_station="5501")])
    response = FavoriteService().find_by_id(1)
    assert response[0].id_user == 1
    assert response[0].id_station == "5501"


def test_favorite_already_exists_true():
    """Test for searching if a favorite already exists (case True)"""
    FavoriteDao().list_all = MagicMock(return_value=[Favorite(id_user=1, id_station="5501")])
    response = FavoriteService().favorite_already_exists(favorite)
    assert response is True


def test_favorite_already_exists_false():
    """Test for searching if a favorite already exists (case False)"""
    FavoriteDao().list_all = MagicMock(return_value=[Favorite(id_user=1, id_station="5502")])
    response = FavoriteService().favorite_already_exists(favorite)
    assert response is False
