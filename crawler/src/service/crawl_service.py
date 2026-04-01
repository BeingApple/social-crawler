from src.common.types import BrandAssignee
from src.common.utils import yesterday_range
from src.resource.repository import (
    SocialCrawlAccountRepository,
    SocialCrawlExcludeKeywordRepository,
    SocialPostCrawlRepository,
)
from src.notifier.slack import SlackNotifier
from src.social.instagram import InstagramCrawler


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

        self.instagram = InstagramCrawler(headless=True)
        #self.tiktok = TikTokCrawler()
        #self.twitter = TwitterCrawler()

        #self.filter = ContentFilter()
        #self.summary_service = SummaryService()
        #self.monitoring = MonitoringService()

    def run(self) -> dict:
        start_dt, end_dt = yesterday_range()



        total_found = 0
        total_saved = 0

        platforms = self.account_repo.social_list()
        available_crawlers = {
            "instagram": self.instagram,
            #"tiktok": self.tiktok,
            #"twitter": self.twitter,
        }

        crawler_map = {
            p.platform_id: available_crawlers[p.platform_id]
            for p in platforms
            if p.platform_id in available_crawlers
        }

        for platform, crawler in crawler_map.items():
            print(f"#platform : " + platform)
            targets = self.account_repo.brand_social_list(platform)
            #targets = self._get_test_targets()  #Test
            print(f"#platform: " + platform + ", #targets: " + str(len(targets)))

            for target in targets:
                #handle = getattr(target, f"{platform}_handle", None)
                handle = target.account_id
                print(f"@platform: {platform}, platform_id: {handle}")

                if not handle:
                    continue

                #self.monitoring.log_start(target.brand_name, platform)

                try:
                    posts = crawler.crawl(
                        brand_name=target.brand_name,
                        handle=handle,
                        search_keywords=[],
                        start_dt=start_dt,
                        end_dt=end_dt,
                    )

                    # TODO: DB 이관 후 brand_id를 brand 테이블에서 조회하여 전달
                    junk_keywords = self.keyword_repo.list_junk_keywords(platform, None)
                    filtered_posts = [
                        p for p in posts
                        if not self.filter.should_skip(p.text_content, junk_keywords)
                    ]

                    saved_posts = []
                    for post in filtered_posts:
                        if self.post_repo.exists(post.platform_id, post.post_id):
                            continue
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
    def _get_test_targets() -> list[BrandAssignee]:
        return [
            BrandAssignee(
                brand_id="인스타그램",
                platform_id="instagram",  #platform_id="musinsa.official",
                assignee_name="test",
                account_id="test",
                account_type="HQ",
                is_active=1
            )
        ]