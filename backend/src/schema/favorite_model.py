from pydantic import BaseModel


class FavoriteAddModel(BaseModel):
    id_user: int
    id_station: str


class FavoriteDeleteModel(BaseModel):
    id_station: str


class ListFavoritesModel(BaseModel):
    favorites: list[dict]
