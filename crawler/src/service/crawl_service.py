import asyncio
import logging
import random

from src.common.encryption import AesDecryptionUtil
from src.common.types import BrandAssigneeWithBrand
from src.common.utils import yesterday_range
from src.resource.repository import (
    SocialCrawlAccountRepository,
    SocialCrawlExcludeKeywordRepository,
    SocialPostCrawlRepository,
)
from src.service.summary_service import ContentFilter
from src.notifier.slack import SlackNotifier
from src.social.instagram import InstagramCrawler

logger = logging.getLogger(__name__)


class CrawlService:
    def __init__(
            self,
            account_repo: SocialCrawlAccountRepository,
            post_repo: SocialPostCrawlRepository,
            keyword_repo: SocialCrawlExcludeKeywordRepository,
            notifier: SlackNotifier,
    ):
        self.account_repo = account_repo
        self.post_repo = post_repo
        self.keyword_repo = keyword_repo
        self.notifier = notifier

        self._decryption = AesDecryptionUtil()

        #self.tiktok = TikTokCrawler()
        #self.twitter = TwitterCrawler()

        self.filter = ContentFilter()
        #self.summary_service = SummaryService()
        #self.monitoring = MonitoringService()

    def _pick_random_crawl_account(self, platform_id: str) -> tuple[str, str] | None:
        """platform_id에 맞는 ACTIVE 계정을 무작위 순서로 시도하여 복호화된 (login_id, login_pw) 반환.

        복호화에 실패한 계정은 건너뛰고 다음 계정을 시도한다.
        반환값이 None이면 사용 가능한 계정이 없거나 모든 계정의 복호화에 실패한 경우다.
        """
        accounts = self.account_repo.list_active(platform_id)
        if not accounts:
            logger.warning("no active crawl account found for platform: %s", platform_id)
            return None

        shuffled = list(accounts)
        random.shuffle(shuffled)

        for account in shuffled:
            logger.info(
                "trying crawl account: name=%s platform=%s",
                account.name, account.platform_id,
            )
            try:
                login_id = self._decryption.decrypt(account.login_id)
                login_pw = self._decryption.decrypt(account.login_pw)
                return login_id, login_pw
            except Exception as e:
                logger.error(
                    "failed to decrypt credentials for account %s (platform=%s): %s: %s",
                    account.name, platform_id, type(e).__name__, e or "(no message)",
                )
                continue

        logger.error(
            "all %d active account(s) for platform=%s failed decryption; check ENCRYPTION_SECRET_KEY",
            len(accounts), platform_id,
        )
        return None

    async def _crawl_platform_async(
            self,
            crawler,
            platform: str,
            platform_targets: list,
            start_dt,
            end_dt,
    ) -> tuple[int, int]:
        """단일 이벤트 루프에서 한 플랫폼의 모든 계정을 순차 크롤링 후 브라우저 종료"""
        total_found = 0
        total_saved = 0

        try:
            for target in platform_targets:
                handle = target.account_id
                logger.info("crawling platform=%s handle=%s brand=%s", platform, handle, target.brand_name)

                try:
                    posts = await crawler._crawl_official_account_async(
                        brand_name=target.brand_name,
                        handle=handle,
                        search_keywords=[],
                        start_dt=start_dt,
                        end_dt=end_dt,
                    )

                    # brand_social_channel.region → account_type 주입
                    for post in posts:
                        post.account_type = target.region or 'HQ'

                    # TODO: DB 이관 후 brand_id를 brand 테이블에서 조회하여 전달
                    junk_keywords = self.keyword_repo.list_junk_keywords(platform, None)
                    filtered_posts = [
                        p for p in posts
                        if not self.filter.should_skip(p.text_content, junk_keywords)
                    ]

                    saved_posts = []
                    for post in filtered_posts:
                        self.post_repo.save(post)
                        saved_posts.append(post)

                    self.post_repo.commit()

                    total_found += len(filtered_posts)
                    total_saved += len(saved_posts)

                    '''
                    if saved_posts:
                        summary = self.summary_service.summarize(target.brand_name, saved_posts)
                        self.notifier.send_summary(
                            brand_name=target.brand_name,
                            platform=platform,
                            posts=saved_posts,
                            ai_summary=summary,
                        )
                    '''

                except Exception as e:
                    print(e)
        finally:
            await crawler.close()

        return total_found, total_saved

    def run(self) -> dict:
        start_dt, end_dt = yesterday_range()

        total_found = 0
        total_saved = 0

        # 구현된 크롤러 맵
        crawler_classes: dict[str, type] = {
            "instagram": InstagramCrawler,
            #"tiktok": TikTokCrawler,
            #"twitter": TwitterCrawler,
        }

        for platform, crawler_cls in crawler_classes.items():
            # 해당 플랫폼의 ACTIVE 크롤 계정을 DB에서 조회해 랜덤 선택 후 복호화
            creds = self._pick_random_crawl_account(platform)
            if creds is None:
                logger.warning("skipping platform=%s: no usable crawl account", platform)
                continue

            username, password = creds
            crawler = crawler_cls(headless=False, username=username, password=password)

            # DB에서 해당 플랫폼의 활성 브랜드 담당자 목록 조회
            platform_targets = self.account_repo.brand_social_list(platform)
            logger.info("platform=%s targets=%d", platform, len(platform_targets))

            # 단일 이벤트 루프에서 해당 플랫폼의 모든 계정 크롤링 (stale context 방지)
            found, saved = asyncio.run(
                self._crawl_platform_async(crawler, platform, platform_targets, start_dt, end_dt)
            )
            total_found += found
            total_saved += saved

        return {
            "status": "ok",
            "found": total_found,
            "saved": total_saved,
        }

