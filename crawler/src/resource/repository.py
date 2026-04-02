import json
from sqlalchemy import or_, select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session

from src.common.types import CrawlAccount, SocialPost, BrandAssigneeWithBrand
from src.resource.models import Brand, BrandSocialChannel, SocialCrawlAccount, SocialCrawlExcludeKeyword, SocialPostCrawl, SocialPlatform, BrandAssignee


class SocialCrawlAccountRepository:

    def __init__(self, session: Session):
        self.session = session

    """크롤링 Social 조회 (social_platform)."""
    def social_list(self) -> list[SocialPlatform]:
        stmt = select(SocialPlatform).where(SocialPlatform.is_active == 1)

        rows = self.session.execute(stmt).scalars().all()
        return [
            SocialPlatform(
                platform_id=row.platform_id,
                platform_name=row.platform_name,
                created_at=row.created_at,
            )
            for row in rows
        ]

    """크롤링용 로그인 계정 조회 (social_crawl_account)."""
    def list_active(self, platform_id: str | None = None) -> list[CrawlAccount]:
        stmt = select(SocialCrawlAccount).where(SocialCrawlAccount.status == "ACTIVE")

        if platform_id:
            stmt = stmt.where(SocialCrawlAccount.platform_id == platform_id)

        rows = self.session.execute(stmt).scalars().all()
        return [
            CrawlAccount(
                account_id=row.account_id,
                name=row.name,
                platform_id=row.platform_id,
                login_id=row.login_id,
                login_pw=row.login_pw,
                status=row.status,
            )
            for row in rows
        ]

    """크롤링용 Brand 조회 (brand_assignee JOIN brand JOIN brand_social_channel)."""
    def brand_social_list(self, platform_id: str | None = None) -> list[BrandAssigneeWithBrand]:
        stmt = (
            select(BrandAssignee, Brand.brand_name, BrandSocialChannel.region)
            .join(Brand, BrandAssignee.brand_id == Brand.brand_id)
            .outerjoin(
                BrandSocialChannel,
                (BrandAssignee.brand_id == BrandSocialChannel.brand_id)
                & (BrandAssignee.platform_id == BrandSocialChannel.platform_id),
            )
            .where(BrandAssignee.is_active == 1)
        )

        if platform_id:
            stmt = stmt.where(BrandAssignee.platform_id == platform_id)

        rows = self.session.execute(stmt).all()

        return [
            BrandAssigneeWithBrand(
                assignee_id=assignee.assignee_id,
                brand_id=assignee.brand_id,
                brand_name=brand_name,
                platform_id=assignee.platform_id,
                assignee_name=assignee.assignee_name,
                account_id=assignee.account_id,
                region=region,
                is_active=assignee.is_active,
            )
            for assignee, brand_name, region in rows
        ]


class SocialPostCrawlRepository:
    """소셜 미디어 게시물 수집 데이터 저장/조회 (social_post_crawl)."""

    def __init__(self, session: Session):
        self.session = session

    def save(self, post: SocialPost) -> None:
        values = dict(
            platform_id=post.platform_id,
            crawl_case=post.crawl_case,
            brand_name=post.brand_name,
            account_id=post.account_id,
            account_type=post.account_type,
            post_id=post.post_id,
            post_url=post.post_url,
            post_type=post.post_type,
            posted_at=post.posted_at,
            post_title=post.post_title,
            text_content=post.text_content,
            person_tags=json.dumps(post.person_tags, ensure_ascii=False) if post.person_tags else None,
            hashtags=json.dumps(post.hashtags, ensure_ascii=False) if post.hashtags else None,
            media_url=post.media_url,
            thumbnail_url=post.thumbnail_url,
            view_count=post.view_count,
            like_count=post.like_count,
            comment_count=post.comment_count,
            share_count=post.share_count,
            matched_keywords=json.dumps(post.matched_keywords, ensure_ascii=False) if post.matched_keywords else None,
            author_name=post.author_name,
            author_followers=post.author_followers,
            raw_data=post.raw_data,
        )
        stmt = insert(SocialPostCrawl).values(**values)
        stmt = stmt.on_duplicate_key_update(
            post_url=stmt.inserted.post_url,
            post_type=stmt.inserted.post_type,
            post_title=stmt.inserted.post_title,
            text_content=stmt.inserted.text_content,
            person_tags=stmt.inserted.person_tags,
            hashtags=stmt.inserted.hashtags,
            media_url=stmt.inserted.media_url,
            thumbnail_url=stmt.inserted.thumbnail_url,
            view_count=stmt.inserted.view_count,
            like_count=stmt.inserted.like_count,
            comment_count=stmt.inserted.comment_count,
            share_count=stmt.inserted.share_count,
            matched_keywords=stmt.inserted.matched_keywords,
            author_followers=stmt.inserted.author_followers,
            raw_data=stmt.inserted.raw_data,
        )
        self.session.execute(stmt)

    def commit(self) -> None:
        self.session.commit()


class SocialCrawlExcludeKeywordRepository:
    """필터 키워드 조회 (social_crawl_exclude_keyword)."""

    def __init__(self, session: Session):
        self.session = session

    def list_junk_keywords(
        self,
        platform_id: str | None = None,
        brand_id: int | None = None,
    ) -> list[str]:
        """정크 키워드 목록 반환 (keyword_type=JUNK)."""
        stmt = (
            select(SocialCrawlExcludeKeyword.junk_keyword)
            .where(
                SocialCrawlExcludeKeyword.is_active == 1,
                SocialCrawlExcludeKeyword.keyword_type == "JUNK",
                SocialCrawlExcludeKeyword.junk_keyword.is_not(None),
                SocialCrawlExcludeKeyword.platform_id == platform_id,
                or_(
                    SocialCrawlExcludeKeyword.brand_id.is_(None),
                    SocialCrawlExcludeKeyword.brand_id == brand_id,
                ),
            )
        )
        return [row for row in self.session.execute(stmt).scalars().all()]

    def list_filter_keywords(
        self,
        platform_id: str | None = None,
        brand_id: int | None = None,
    ) -> list[str]:
        """CASE2 수집 필터 키워드 목록 반환 (keyword_type=CASE2_FILTER)."""
        stmt = (
            select(SocialCrawlExcludeKeyword.filter_keyword)
            .where(
                SocialCrawlExcludeKeyword.is_active == 1,
                SocialCrawlExcludeKeyword.keyword_type == "CASE2_FILTER",
                SocialCrawlExcludeKeyword.filter_keyword.is_not(None),
                SocialCrawlExcludeKeyword.platform_id == platform_id,
                or_(
                    SocialCrawlExcludeKeyword.brand_id.is_(None),
                    SocialCrawlExcludeKeyword.brand_id == brand_id,
                ),
            )
        )
        return [row for row in self.session.execute(stmt).scalars().all()]