from abc import ABC, abstractmethod
from datetime import datetime

from src.common.types import SocialPost


class BaseCrawler(ABC):
    platform: str

    @abstractmethod
    def crawl_official_account(
            self,
            brand_name: str,
            handle: str,
            account_type: str,
            search_keywords: list[str],
            start_dt: datetime,
            end_dt: datetime,
    ) -> list[SocialPost]:
        raise NotImplementedError

    @abstractmethod
    def crawl_search(
            self,
            brand_name: str,
            account_type: str,
            search_keywords: list[str],
            start_dt: datetime,
            end_dt: datetime,
    ) -> list[SocialPost]:
        raise NotImplementedError

    def crawl(
            self,
            brand_name: str,
            handle: str | None,
            account_type: str,
            search_keywords: list[str],
            start_dt: datetime,
            end_dt: datetime,
    ) -> list[SocialPost]:
        results: list[SocialPost] = []

        if handle:
            results.extend(self.crawl_official_account(brand_name, handle, account_type, search_keywords, start_dt, end_dt))

        # TODO : 검색어 추후 확인
        #results.extend(self.crawl_search(brand_name, account_type, search_keywords, start_dt, end_dt))

        deduped: dict[str, SocialPost] = {}
        for post in results:
            deduped[post.post_id] = post

        return list(deduped.values())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(platform={self.platform!r})"