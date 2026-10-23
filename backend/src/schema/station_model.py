from pydantic import BaseModel


class StationReadModel(BaseModel):
    id_station: int
    name: str
    lat: float
    lon: float
    capacity: int | None
    fill_rate: float | None
    shortage_rate: float | None
    saturation_rate: float | None
    shortage_mean_time: float | None
    saturation_mean_time: float | None


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
