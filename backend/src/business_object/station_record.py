from datetime import datetime


class StationRecord:
    """Snapshot of a station's availability at a given time."""

    def __init__(
        self,
        id_station: int,
        date: datetime,
        status: str,
        nb_available_spaces: int,
        nb_available_bikes: int,
        nb_available_ebikes: int | None = None,
    ):
        """Constructor"""
        self.id_station = id_station
        self.date = date
        self.status = status
        self.nb_available_spaces = nb_available_spaces
        self.nb_available_bikes = nb_available_bikes
        self.nb_available_ebikes = nb_available_ebikes
