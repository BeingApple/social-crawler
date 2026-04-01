"""
엔트리포인트 — schedule 라이브러리로 주기적 크롤 실행.
CRAWL_INTERVAL_SEC 환경변수로 주기 조절 (기본 3600초 = 1시간).
"""
import logging
import os

import schedule
import time

from dotenv import load_dotenv
from pathlib import Path
from src.resource.db import SessionLocal
from src.resource.repository import (
    SocialCrawlAccountRepository,
    SocialCrawlExcludeKeywordRepository,
    SocialPostCrawlRepository,
)
from src.notifier.slack import SlackNotifier
from src.service.crawl_service import CrawlService

# 프로그램 시작 시 .env 로드
_BASE_DIR = Path(__file__).resolve().parent.parent
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
    run_all()

    # 이후 주기 실행
    #schedule.every(INTERVAL).seconds.do(run_all)

    #while True:
    #    schedule.run_pending()
    #    time.sleep(10)


def run_all():
    session = SessionLocal()
    try:
        service = CrawlService(
            account_repo=SocialCrawlAccountRepository(session),
            post_repo=SocialPostCrawlRepository(session),
            keyword_repo=SocialCrawlExcludeKeywordRepository(session),
            notifier=SlackNotifier(None), #notifier=SlackNotifier(os.environ["SLACK_WEBHOOK_URL"]),
        )
        service.run()
    finally:
        session.close()


def run_all_test():
    session = SessionLocal()
    try:
        service = CrawlService(
            account_repo=SocialCrawlAccountRepository(session),
            post_repo=SocialPostCrawlRepository(session),
            keyword_repo=SocialCrawlExcludeKeywordRepository(session),
            notifier=SlackNotifier(None),
        )
        service.run()
    finally:
        session.close()


if __name__ == "__main__":
    main()