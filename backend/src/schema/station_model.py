from pydantic import BaseModel


class StationReadModel(BaseModel):
    id_station: int
    name: str
    lat: float
    lon: float
    capacity: int | None


class FavoriteAddModel(BaseModel):
    id_user: int
    id_station: int


class FavoriteDeleteModel(BaseModel):
    id_station: int


class Statistics(BaseModel):
    fill_rate: float
    shortage_rate: float
    saturation_rate: float
    shortage_mean_time: float
    saturation_mean_time: float
