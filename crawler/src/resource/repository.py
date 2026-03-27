from pymysql.cursors import DictCursor

from src.common.types import BrandTarget, SocialPost


class BrandRepository:
    def __init__(self, conn):
        self.conn = conn

    def list_active_targets(self) -> list[BrandTarget]:
        '''
        sql = """
              SELECT
                  id, brand_name,
                  instagram_handle, tiktok_username, twitter_handle,
                  search_keywords, junk_keywords
              FROM brands
              WHERE is_active = 1 \
              """
        '''
        sql = """
              SELECT
                  1 as id
                    ,'2' as  brand_name
                    ,'musinsa.official' as instagram_handle
                    ,'4' as tiktok_username
                    ,'5' as twitter_handle
                    ,'6' as search_keywords
                    ,'7' as junk_keywords
              """
        with self.conn.cursor(DictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()

        return [
            BrandTarget(
                id=row["id"],
                brand_name=row["brand_name"],
                instagram_handle=row.get("instagram_handle"),
                tiktok_username=row.get("tiktok_username"),
                twitter_handle=row.get("twitter_handle"),
                search_keywords=row.get("search_keywords") or [],
                junk_keywords=row.get("junk_keywords") or [],
                is_active=True,
            )
            for row in rows
        ]

    def list_active_targets_test(self) -> list[BrandTarget]:
        return [
            BrandTarget(
                id=12391,
                brand_name='bbbb',
                instagram_handle='instagram',
                tiktok_username='dddd',
                twitter_handle='eeeee',
                search_keywords='ffff' or [],
                junk_keywords='ggggg' or [],
                is_active=True,
            )
        ]

    def list_active_instagram_targets(self) -> list[BrandTarget]:
        sql = """
              SELECT
                  id, brand_name,
                  instagram_handle, search_keywords, junk_keywords
              FROM brands
              WHERE is_active = 1
                AND instagram_handle IS NOT NULL \
              """
        with self.conn.cursor(DictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()

        return [
            BrandTarget(
                id=row["id"],
                brand_name=row["brand_name"],
                instagram_handle=row.get("instagram_handle"),
                search_keywords=row.get("search_keywords") or [],
                junk_keywords=row.get("junk_keywords") or [],
            )
            for row in rows
        ]


class SocialPostRepository:
    def __init__(self, conn):
        self.conn = conn

    def exists(self, platform: str, external_post_id: str) -> bool:
        sql = """
              SELECT 1
              FROM social_posts
              WHERE platform = %s AND external_post_id = %s
                  LIMIT 1 \
              """
        with self.conn.cursor() as cur:
            cur.execute(sql, (platform, external_post_id))
            return cur.fetchone() is not None

    def save(self, post: SocialPost) -> None:
        sql = """
              INSERT INTO social_posts (
                  brand_id, platform, external_post_id, post_url,
                  content, likes, comments, shares, views,
                  posted_at, crawled_at
              )
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                  ON DUPLICATE KEY UPDATE
                                       post_url = VALUES(post_url),
                                       content = VALUES(content),
                                       likes = VALUES(likes),
                                       comments = VALUES(comments),
                                       shares = VALUES(shares),
                                       views = VALUES(views),
                                       posted_at = VALUES(posted_at),
                                       crawled_at = NOW() \
              """
        with self.conn.cursor() as cur:
            cur.execute(sql, (
                post.brand_id,
                post.platform,
                post.external_post_id,
                post.post_url,
                post.content,
                post.likes,
                post.comments,
                post.shares,
                post.views,
                post.posted_at,
            ))

    def commit(self) -> None:
        self.conn.commit()


class CrawlJobRepository:
    def __init__(self, conn):
        self.conn = conn

    def start(self, brand_id: int, platform: str) -> int:
        sql = """
              INSERT INTO crawl_jobs (brand_id, platform, status, started_at)
              VALUES (%s, %s, 'running', NOW()) \
              """
        with self.conn.cursor() as cur:
            cur.execute(sql, (brand_id, platform))
            return cur.lastrowid

    def finish(self, job_id: int, status: str, found: int, saved: int, error_message: str | None = None) -> None:
        sql = """
              UPDATE crawl_jobs
              SET finished_at = NOW(),
                  status = %s,
                  items_found = %s,
                  items_saved = %s,
                  error_message = %s,
                  finished_at = NOW()
              WHERE id = %s \
              """
        with self.conn.cursor() as cur:
            cur.execute(sql, (status, found, saved, error_message, job_id))

    def commit(self) -> None:
        self.conn.commit()