from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BrandConfig:
    """크롤링 대상 브랜드 설정 (임시 — 향후 DB 테이블로 이관 예정).

    DB 이관 시 각 필드 출처:
      brand_name      → brand.brand_name
      instagram_handle→ brand_assignee.account_id  (platform_id='instagram')
      search_keywords → social_crawl_exclude_keyword (keyword_type='CASE2_FILTER')
    """

    brand_name: str
    instagram_handle: str | None = None          # → brand_assignee.account_id (platform_id='instagram')
    search_keywords: list[str] = field(default_factory=list)  # → social_crawl_exclude_keyword (CASE2_FILTER)


@dataclass
class CrawlAccount:
    """크롤링용 로그인 계정 (social_crawl_account)."""

    account_id: int
    name: str
    platform_id: str
    login_id: str
    login_pw: str
    status: str


@dataclass
class SocialPost:
    """수집된 소셜 게시물 (social_post_crawl)."""

    # 수집 메타
    platform_id: str
    crawl_case: str           # CASE1: 공식계정 | CASE2: 키워드검색
    brand_name: str
    account_id: str

    # 게시물 정보
    post_id: str
    post_url: str
    posted_at: datetime

    post_type: str | None = None
    post_title: str | None = None
    text_content: str | None = None
    person_tags: list[str] = field(default_factory=list)
    hashtags: list[str] = field(default_factory=list)
    media_url: str | None = None

    # 통계
    view_count: int | None = None
    like_count: int | None = None
    comment_count: int | None = None
    share_count: int | None = None

    # CASE2 전용
    matched_keywords: list[str] = field(default_factory=list)
    author_name: str | None = None
    author_followers: int | None = None

    # 원본
    raw_data: dict | None = None

    @property
    def is_valid(self) -> bool:
        return bool(
            self.platform_id and self.brand_name and self.account_id
            and self.post_id and self.post_url and self.posted_at
        )