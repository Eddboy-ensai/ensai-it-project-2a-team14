from pydantic import BaseModel


class StationReadModel(BaseModel):
    id_station: int
    name: str
    lat: float
    lon: float
    capacity: int | None
