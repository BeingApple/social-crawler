from dataclasses import dataclass, field

from src.common.utils import yesterday_range
from src.resource.repository import (
    SocialCrawlAccountRepository,
    SocialCrawlExcludeKeywordRepository,
    SocialPostCrawlRepository,
)
from src.notifier.slack import SlackNotifier
from src.social.instagram import InstagramCrawler


@dataclass
class BrandConfig:
    """크롤링 대상 브랜드 설정 (임시 — 향후 DB 테이블로 이관 예정)."""

    brand_id: int
    brand_name: str                              # 로깅/모니터링용
    account_type: str                            # KR | HQ
    instagram_handle: str | None = None
    search_keywords: list[str] = field(default_factory=list)


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

        self.instagram = InstagramCrawler(headless=False)
        #self.tiktok = TikTokCrawler()
        #self.twitter = TwitterCrawler()

        #self.filter = ContentFilter()
        #self.summary_service = SummaryService()
        #self.monitoring = MonitoringService()

    def run(self) -> dict:
        start_dt, end_dt = yesterday_range()
        targets = self._get_test_targets()  # TODO: DB 기반 브랜드 설정 테이블로 교체

        total_found = 0
        total_saved = 0

        crawler_map = {
            "instagram": self.instagram,
            #"tiktok": self.tiktok,
            #"twitter": self.twitter,
        }

        for target in targets:
            for platform, crawler in crawler_map.items():
                handle = getattr(target, f"{platform}_handle", None)
                if not handle:
                    continue

                #self.monitoring.log_start(target.brand_name, platform)

                try:
                    posts = crawler.crawl(
                        brand_id=target.brand_id,
                        handle=handle,
                        account_type=target.account_type,
                        search_keywords=target.search_keywords,
                        start_dt=start_dt,
                        end_dt=end_dt,
                    )

                    '''
                    junk_keywords = self.keyword_repo.list_junk_keywords(platform, target.brand_id)
                    filtered_posts = [
                        p for p in posts
                        if not self.filter.should_skip(p.text_content, junk_keywords)
                    ]

                    saved_posts = []
                    for post in filtered_posts:
                        if self.post_repo.exists(post.platform, post.post_id):
                            continue
                        self.post_repo.save(post)
                        saved_posts.append(post)

                    self.post_repo.commit()

                    total_found += len(filtered_posts)
                    total_saved += len(saved_posts)

                    if saved_posts:
                        summary = self.summary_service.summarize(target.brand_name, saved_posts)
                        self.notifier.send_summary(
                            brand_name=target.brand_name,
                            platform=platform,
                            posts=saved_posts,
                            ai_summary=summary,
                        )
                    '''

                    #self.monitoring.log_result(target.brand_name, platform, len(filtered_posts), len(saved_posts))

                except Exception as e:
                    print(e)
                    #self.post_repo.session.rollback()
                    #self.monitoring.log_error(target.brand_name, platform, e)

        return {
            "status": "ok",
            "found": total_found,
            "saved": total_saved,
        }

    @staticmethod
    def _get_test_targets() -> list[BrandConfig]:
        return [
            BrandConfig(
                brand_id=1,
                brand_name="인스타그램",
                account_type="KR",
                instagram_handle="instagram",
                #instagram_handle="musinsa.official",
                search_keywords=[],
            )
        ]