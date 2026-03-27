from time import perf_counter
import logging

logger = logging.getLogger(__name__)


class MonitoringService:
    def __init__(self):
        self.started_at = perf_counter()

    def log_start(self, brand_name: str, platform: str) -> None:
        logger.info("crawl_start brand=%s platform=%s", brand_name, platform)

    def log_result(self, brand_name: str, platform: str, found: int, saved: int) -> None:
        logger.info(
            "crawl_result brand=%s platform=%s found=%s saved=%s",
            brand_name, platform, found, saved
        )

    def log_error(self, brand_name: str, platform: str, error: Exception) -> None:
        logger.exception("crawl_error brand=%s platform=%s error=%s", brand_name, platform, error)

    def elapsed_ms(self) -> int:
        return int((perf_counter() - self.started_at) * 1000)