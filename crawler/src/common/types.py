from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BrandTarget:
    id: int
    brand_name: str
    instagram_handle: str | None = None
    tiktok_username: str | None = None
    twitter_handle: str | None = None
    search_keywords: list[str] = field(default_factory=list)
    junk_keywords: list[str] = field(default_factory=list)
    is_active: bool = True


@dataclass
class SocialPost:
    brand_id: int
    platform: str
    external_post_id: str
    post_url: str
    content: str
    likes: int = 0
    comments: int = 0
    shares: int = 0
    views: int = 0
    posted_at: datetime | None = None
    crawled_at: datetime | None = None
    matched_keywords: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.brand_id > 0 and self.platform and self.external_post_id and self.post_url and self.content