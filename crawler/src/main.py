"""
엔트리포인트 — schedule 라이브러리로 주기적 크롤 실행.
CRAWL_INTERVAL_SEC 환경변수로 주기 조절 (기본 3600초 = 1시간).
"""
import logging
import os
import time

import schedule

from src.crawler import run_all

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)

logger = logging.getLogger(__name__)
INTERVAL = int(os.environ.get("CRAWL_INTERVAL_SEC", "3600"))


def main() -> None:
    logger.info("Crawler started. Interval=%ds", INTERVAL)

    # 시작 즉시 1회 실행
    run_all()

    # 이후 주기 실행
    schedule.every(INTERVAL).seconds.do(run_all)

    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    main()
