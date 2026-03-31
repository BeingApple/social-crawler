from src.common.utils import yesterday_range
from src.resource.repository import BrandRepository, SocialPostRepository, CrawlJobRepository
from src.notifier.slack import SlackNotifier
from src.social.instagram import InstagramCrawler


class CrawlService:
    def __init__(
            self,
            brand_repo: BrandRepository,
            post_repo: SocialPostRepository,
            job_repo: CrawlJobRepository,
            notifier: SlackNotifier,
    ):
        self.brand_repo = brand_repo
        self.post_repo = post_repo
        self.job_repo = job_repo
        self.notifier = notifier

        self.instagram = InstagramCrawler()
        #self.tiktok = TikTokCrawler()
        #self.twitter = TwitterCrawler()

        #self.filter = ContentFilter()
        #self.summary_service = SummaryService()
        #self.monitoring = MonitoringService()

    def run(self) -> dict:
        start_dt, end_dt = yesterday_range()
        #targets = self.brand_repo.list_active_targets() #hsgtest
        targets = self.brand_repo.list_active_targets_test()

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
                if not handle and platform != "twitter":
                    continue
                if platform == "twitter" and not handle:
                    continue

                #job_id = self.job_repo.start(target.id, platform) #test
                #self.monitoring.log_start(target.brand_name, platform)

                try:
                    posts = crawler.crawl(
                        brand_id=target.id,
                        handle=handle,
                        search_keywords=target.search_keywords,
                        start_dt=start_dt,
                        end_dt=end_dt,
                    )

                    '''
                    filtered_posts = [
                        p for p in posts
                        if not self.filter.should_skip(p.content, target.junk_keywords)
                    ]

                    saved_posts = []
                    for post in filtered_posts:
                        if self.post_repo.exists(post.platform, post.external_post_id):
                            continue
                        #self.post_repo.save(post) # test save
                        saved_posts.append(post)
                    '''

                    # self.post_repo.commit() #test

                    #total_found += len(filtered_posts)
                    #total_saved += len(saved_posts)

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
                    #self.job_repo.finish(job_id, "success", len(filtered_posts), len(saved_posts))
                    #self.job_repo.commit()

                    #self.monitoring.log_result(target.brand_name, platform, len(filtered_posts), len(saved_posts))

                except Exception as e:
                    print(e)
                    #self.post_repo.conn.rollback()
                    #self.job_repo.finish(job_id, "failed", 0, 0, str(e))
                    #self.job_repo.commit()
                    #self.monitoring.log_error(target.brand_name, platform, e)

        return {
            "status": "ok",
            "found": total_found,
            "saved": total_saved,
        }