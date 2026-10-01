import requests

from utils.log_utils import get_logger, log
from utils.singleton import Singleton

logger = get_logger(__name__)

URL_STATUS = "https://eu.ftp.opendatasoft.com/star/gbfs/station_status.json"
URL_INFO = "https://eu.ftp.opendatasoft.com/star/gbfs/station_information.json"


class GbfsDao(metaclass=Singleton):
    """Access to the STAR bike-sharing open data (GBFS feeds)."""

    @log
    def get_station_information(self) -> dict:
        """Returns the raw station_information JSON (list of stations)."""
        return self._get_json(URL_INFO)

    @log
    def get_station_status(self) -> dict:
        """Returns the raw station_status JSON (current availability)."""
        return self._get_json(URL_STATUS)

    @staticmethod
    def _get_json(url: str) -> dict:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()