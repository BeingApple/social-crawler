"""SQLAlchemy ORM 모델 — DB 스키마와 동일.

기준: brand_sns_schema_20260331.xlsx + 1차개발항목테이블_20260331_수정.xlsx
"""
from datetime import datetime, UTC
from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, SmallInteger, String, Text, JSON, UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from src.resource.db import Base


class SocialPlatform(Base):
    """SNS 플랫폼 마스터."""

    __tablename__ = "social_platform"
    __table_args__ = (
        {"comment": "SNS 플랫폼 마스터"},
    )

    platform_id:   Mapped[str]      = mapped_column(String(50),  primary_key=True, comment="플랫폼 식별키 (instagram, youtube, x, tiktok)")
    platform_name: Mapped[str]      = mapped_column(String(100), nullable=False,   comment="플랫폼 표시명")
    created_at:    Mapped[datetime] = mapped_column(DateTime,    nullable=False,   default=lambda: datetime.now(UTC))


class Brand(Base):
    """브랜드 기본 정보."""

    __tablename__ = "brand"
    __table_args__ = (
        {"comment": "브랜드 기본 정보"},
    )

    brand_id:   Mapped[int]      = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    brand_name: Mapped[str]      = mapped_column(String(100), nullable=False, comment="브랜드 표시명")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


class BrandSocialChannel(Base):
    """브랜드 SNS 채널 (브랜드 × 플랫폼 × 지역 매핑)."""

    __tablename__ = "brand_social_channel"
    __table_args__ = (
        UniqueConstraint("brand_id", "platform_id", "region", name="uq_brand_platform_region"),
        {"comment": "브랜드 SNS 채널 정보 (브랜드 + 플랫폼 + 지역 UNIQUE)"},
    )

    channel_id:  Mapped[int]      = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    brand_id:    Mapped[int]      = mapped_column(BigInteger, ForeignKey("brand.brand_id", ondelete="CASCADE"), nullable=False, comment="brand.brand_id 참조")
    platform_id: Mapped[str]      = mapped_column(String(50), ForeignKey("social_platform.platform_id"), nullable=False, comment="social_platform.platform_id 참조")
    region:      Mapped[str]      = mapped_column(String(10), nullable=False, comment="지역 구분 (KR, HQ 등)")
    channel_url: Mapped[str|None] = mapped_column(String(200), comment="SNS 채널 전체 URL (미등록 시 NULL)")
    created_at:  Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at:  Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


class BrandAssignee(Base):
    """브랜드 담당자 정보."""

    __tablename__ = "brand_assignee"
    __table_args__ = (
        {"comment": "브랜드 담당자 정보"},
    )

    assignee_id:   Mapped[int]      = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    brand_id:      Mapped[int]      = mapped_column(BigInteger, ForeignKey("brand.brand_id", ondelete="CASCADE"), nullable=False, comment="brand.brand_id 참조")
    platform_id:   Mapped[str]      = mapped_column(String(50), ForeignKey("social_platform.platform_id"), nullable=False, comment="social_platform.platform_id 참조")
    assignee_name: Mapped[str]      = mapped_column(String(50),  nullable=False, comment="담당자명")
    account_id:    Mapped[str]      = mapped_column(String(100), nullable=False, comment="소셜 미디어 계정 아이디")
    is_active:     Mapped[int]      = mapped_column(SmallInteger, nullable=False, default=1, comment="활성화 상태 (1: 활성, 0: 비활성)")
    created_at:    Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at:    Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


class SocialPostCrawl(Base):
    """소셜 미디어 게시물 수집 데이터."""

    __tablename__ = "social_post_crawl"
    __table_args__ = (
        UniqueConstraint("platform_id", "post_id", name="uq_platform_post"),
        Index("idx_brand_platform", "brand_name", "platform_id"),
        Index("idx_crawl_case",     "crawl_case"),
        Index("idx_posted_at",      "posted_at"),
        Index("idx_is_duplicate",   "is_duplicate"),
        Index("idx_is_junk",        "is_junk"),
        {"comment": "소셜 미디어 브랜드 크롤링 수집 데이터"},
    )

    # 식별자
    spc_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)

    # 수집 메타
    platform_id:  Mapped[str] = mapped_column(String(50),  nullable=False, comment="social_platform.platform_id 참조")
    crawl_case:   Mapped[str] = mapped_column(String(10),  nullable=False, comment="수집 유형 (CASE1: 공식계정, CASE2: 키워드검색)")
    brand_name:   Mapped[str] = mapped_column(String(100), nullable=False, comment="브랜드명")
    account_id:   Mapped[str] = mapped_column(String(200), nullable=False, comment="계정 ID/핸들")
    account_type: Mapped[str] = mapped_column(String(10),  nullable=False, comment="계정 유형 (brand_social_channel.region 참조: KR, HQ 등)")

    # 게시물 정보
    post_id:      Mapped[str]      = mapped_column(String(200), nullable=False, comment="게시물 고유 ID")
    post_url:     Mapped[str]      = mapped_column(String(500), nullable=False, comment="게시물 원본 URL")
    post_type:    Mapped[str|None] = mapped_column(String(30),  comment="게시물 유형 (릴스, 피드, 쇼츠, 영상, 트윗 등)")
    posted_at:    Mapped[datetime] = mapped_column(DateTime,    nullable=False, comment="게시 일시")
    post_title:   Mapped[str|None] = mapped_column(String(255), comment="게시물 제목")
    text_content: Mapped[str|None] = mapped_column(Text,        comment="게시물 텍스트/캡션")
    person_tags:  Mapped[str|None] = mapped_column(Text,        comment="인물태그 목록 (JSON array)")
    hashtags:     Mapped[str|None] = mapped_column(Text,        comment="해시태그 목록 (JSON array)")
    media_url:     Mapped[str|None] = mapped_column(Text, comment="미디어(이미지/영상) URL (첫 번째 미디어, CDN signed URL로 장문 가능)")
    thumbnail_url: Mapped[str|None] = mapped_column(Text, comment="썸네일 이미지 URL (image_versions2 최소 크기)")

    # 통계
    view_count:    Mapped[int|None] = mapped_column(BigInteger, comment="조회수")
    like_count:    Mapped[int|None] = mapped_column(BigInteger, comment="좋아요 수")
    comment_count: Mapped[int|None] = mapped_column(BigInteger, comment="댓글 수")
    share_count:   Mapped[int|None] = mapped_column(BigInteger, comment="공유/리트윗 수")

    # CASE2 전용
    matched_keywords: Mapped[str|None] = mapped_column(Text,        comment="매칭된 키워드 목록 (JSON array, CASE2 전용)")
    author_name:      Mapped[str|None] = mapped_column(String(200), comment="작성자명 (CASE2: 인플루언서명)")
    author_followers: Mapped[int|None] = mapped_column(BigInteger,  comment="작성자 팔로워 수")

    # 플래그 & 원본
    is_duplicate: Mapped[int]      = mapped_column(SmallInteger, nullable=False, default=0, comment="중복 여부 (0: 정상, 1: 중복)")
    is_junk:      Mapped[int]      = mapped_column(SmallInteger, nullable=False, default=0, comment="정크 여부 (0: 정상, 1: 정크)")
    raw_data:     Mapped[dict|None] = mapped_column(JSON, comment="API 원본 응답 데이터 (재처리 대비 원본 보존)")

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(UTC),    comment="수집 일시")
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), comment="수정 일시")


class SocialCrawlAccount(Base):
    """크롤링용 로그인 계정 관리."""

    __tablename__ = "social_crawl_account"
    __table_args__ = (
        UniqueConstraint("platform_id", "login_id", name="uq_platform_login_id"),
        Index("idx_platform_id", "platform_id"),
        Index("idx_status",      "status"),
        {"comment": "소셜 미디어 크롤링용 로그인 계정 관리"},
    )

    # 식별자
    account_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)

    # 계정 정보
    name:        Mapped[str] = mapped_column(String(100), nullable=False, comment="계정 이름 (담당자명 또는 계정 별칭)")
    platform_id: Mapped[str] = mapped_column(String(50),  nullable=False, comment="social_platform.platform_id 참조")
    login_id:    Mapped[str] = mapped_column(String(200), nullable=False, comment="로그인 ID (암호화 저장 권장)")
    login_pw:    Mapped[str] = mapped_column(String(500), nullable=False, comment="로그인 비밀번호 (AES-256 암호화 필수)")

    # 상태 & 이슈
    issue:  Mapped[str|None] = mapped_column(Text,      comment="이슈 사항 (차단, 세션 만료, 2FA 등)")
    status: Mapped[str]      = mapped_column(String(20), nullable=False, default="ACTIVE", comment="계정 상태 (ACTIVE, BLOCKED, EXPIRED, PAUSED)")

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


class SocialCrawlExcludeKeyword(Base):
    """수집 필터 키워드 관리 (정크 / CASE2)."""

    __tablename__ = "social_crawl_exclude_keyword"
    __table_args__ = (
        Index("idx_keyword_type", "keyword_type"),
        Index("idx_platform_id",  "platform_id"),
        Index("idx_brand_id",     "brand_id"),
        Index("idx_is_active",    "is_active"),
        {"comment": "소셜 미디어 크롤링 필터링 키워드 관리 (정크 / CASE2 수집 필터)"},
    )

    # 식별자
    keyword_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)

    # 키워드 분류
    keyword_type: Mapped[str]      = mapped_column(String(20), nullable=False, comment="키워드 유형 (JUNK, CASE2_FILTER)")
    platform_id:  Mapped[str]      = mapped_column(String(50), nullable=False, comment="social_platform.platform_id 참조")
    brand_id:     Mapped[int|None] = mapped_column(BIGINT(unsigned=True), comment="적용 브랜드 ID (NULL: 전체 공통)")

    # 키워드 내용
    filter_keyword: Mapped[str|None] = mapped_column(String(500), comment="CASE2 수집 필터 키워드 (keyword_type=CASE2_FILTER 시 사용)")
    junk_keyword:   Mapped[str|None] = mapped_column(String(500), comment="정크 필터 키워드 (keyword_type=JUNK 시 사용)")
    match_type:     Mapped[str]      = mapped_column(String(20), nullable=False, default="CONTAINS", comment="매칭 방식 (CONTAINS, EXACT, REGEX)")
    description:    Mapped[str|None] = mapped_column(String(300), comment="등록 사유 / 설명")

    # 상태 & 관리
    is_active:  Mapped[int]      = mapped_column(SmallInteger, nullable=False, default=1, comment="활성화 여부 (0: 비활성, 1: 활성)")
    created_by: Mapped[str|None] = mapped_column(String(100), comment="등록자")

    # 타임스탬프
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))