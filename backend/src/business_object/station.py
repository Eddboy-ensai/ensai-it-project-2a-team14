class Station:
    """Class representing a station"""

    def __init__(
        self, id_station: str, name: str, lat: float, lon: float, capacity: int | None = None
    ):
        """Constructor"""
        self.id_station = id_station
        self.name = name
        self.lat = lat
        self.lon = lon
        self.capacity = capacity
