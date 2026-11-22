from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StationDataModel(BaseModel):
    id_station: str
    name: str
    lat: float
    lon: float
    capacity: int | None
    #status: str
    fill_rate: float | None
    shortage_rate: float | None
    saturation_rate: float | None
    shortage_mean_time: float | None
    saturation_mean_time: float | None
    score: int | None
    availability_spaces: list[dict]
    availability_bikes: list[dict]
    prediction_spaces: int
    prediction_bikes: int


class StationReadModel(BaseModel):
    id_station: str
    name: str
    lat: float
    lon: float
    capacity: int | None


class StationRecordModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: datetime
    status: str | None
    nb_available_bikes: int | None
    nb_available_ebikes: int | None
    nb_available_spaces: int | None


class StationSuggestionModel(BaseModel):
    station: StationReadModel
    score: int


class StationLatestRecordModel(BaseModel):
    nb_available_spaces: int | None
    nb_available_bikes: int | None
