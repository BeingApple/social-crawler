"""
엔트리포인트 — schedule 라이브러리로 주기적 크롤 실행.
CRAWL_INTERVAL_SEC 환경변수로 주기 조절 (기본 3600초 = 1시간).
"""
import logging
import os

import schedule
import time

#from src.crawler import run_all

from dotenv import load_dotenv
from pathlib import Path
from src.resource.repository import BrandRepository, SocialPostRepository, CrawlJobRepository
from src.notifier.slack import SlackNotifier
from src.service.crawl_service import CrawlService
from src.config.database import get_connection

# 프로그램 시작 시 .env 로드
_BASE_DIR = Path(__file__).resolve().parent
load_dotenv(_BASE_DIR / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)

logger = logging.getLogger(__name__)
INTERVAL = int(os.environ.get("CRAWL_INTERVAL_SEC", "3600"))

def main() -> None:
    logger.info("Crawler started. Interval=%ds", INTERVAL)

    # 시작 즉시 1회 실행
    run_all_test()

    # 이후 주기 실행
    #schedule.every(INTERVAL).seconds.do(run_all_test())

    '''
    while True:
        schedule.run_pending()
        time.sleep(10)
    '''
    '''
    return {
        "statusCode": 200,
        "body": json.dumps(result, ensure_ascii=False),
    }
    '''

def run_all():
    conn = None
    try:
        conn = get_connection()

        service = CrawlService(
            brand_repo=BrandRepository(conn),
            post_repo=SocialPostRepository(conn),
            job_repo=CrawlJobRepository(conn),
            notifier=SlackNotifier(os.environ["SLACK_WEBHOOK_URL"]),
        )

        service.run()
    finally:
        conn.close()
        print("close connection")


def run_all_test():
    try:
        service = CrawlService(
            brand_repo=BrandRepository(None),
            post_repo=SocialPostRepository(None),
            job_repo=CrawlJobRepository(None),
            notifier=SlackNotifier(None),
        )

        service.run()
    finally:
        #conn.close()
        print("close connection")

if __name__ == "__main__":
    main()
