import time

from service.collect_service import CollectService
from utils.env_variables import load_environment_variables
from utils.log_utils import get_logger, initialize_logs

INTERVAL = 300

if __name__ == "__main__":
    initialize_logs("Collector")
    load_environment_variables()
    logger = get_logger(__name__)
    service = CollectService()
    while True:
        try:
            service.refresh_stations()
            service.collect_records()
        except Exception:
            logger.exception("Collecte échouée")
        time.sleep(INTERVAL)
