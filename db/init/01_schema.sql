SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- ============================================================
-- brand-social-crawler 스키마
-- Aurora MySQL 8.0 호환
-- 기준: brand_sns_schema_20260331.xlsx + 1차개발항목테이블_20260331_수정.xlsx
-- ============================================================

-- ① SNS 플랫폼 마스터
CREATE TABLE IF NOT EXISTS social_platform (
    platform_id     VARCHAR(50)     NOT NULL COMMENT '플랫폼 식별키 (instagram, youtube, x, tiktok)',
    platform_name   VARCHAR(100)    NOT NULL COMMENT '플랫폼 표시명',
    is_active       TINYINT(1)      NOT NULL DEFAULT 1 COMMENT '활성화 상태 (1: 활성, 0: 비활성)',
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (platform_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='SNS 플랫폼 마스터';

-- ② 브랜드
CREATE TABLE IF NOT EXISTS brand (
    brand_id        BIGINT          NOT NULL AUTO_INCREMENT,
    brand_name      VARCHAR(100)    NOT NULL COMMENT '브랜드 표시명',
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (brand_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='브랜드 기본 정보';

-- ③ 브랜드 SNS 채널 (브랜드 × 플랫폼 × 지역 매핑)
CREATE TABLE IF NOT EXISTS brand_social_channel (
    channel_id      BIGINT          NOT NULL AUTO_INCREMENT,
    brand_id        BIGINT          NOT NULL COMMENT 'brand.brand_idear 참조',
    platform_id     VARCHAR(50)     NOT NULL COMMENT 'social_platform.platform_id 참조',
    region          VARCHAR(10)     NOT NULL COMMENT '지역 구분 (KR, HQ 등)',
    channel_url     VARCHAR(200)    NULL     COMMENT 'SNS 채널 전체 URL (미등록 시 NULL)',
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (channel_id),
    UNIQUE KEY uq_brand_platform_region (brand_id, platform_id, region),
    CONSTRAINT fk_bsc_brand    FOREIGN KEY (brand_id)    REFERENCES brand (brand_id)           ON DELETE CASCADE,
    CONSTRAINT fk_bsc_platform FOREIGN KEY (platform_id) REFERENCES social_platform (platform_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='브랜드 SNS 채널 정보 (브랜드 + 플랫폼 + 지역 UNIQUE)';

-- ④ 브랜드 담당자
CREATE TABLE IF NOT EXISTS brand_assignee (
    assignee_id     BIGINT          NOT NULL AUTO_INCREMENT,
    brand_id        BIGINT          NOT NULL COMMENT 'brand.brand_id 참조',
    platform_id     VARCHAR(50)     NOT NULL COMMENT 'social_platform.platform_id 참조',
    assignee_name   VARCHAR(50)     NOT NULL COMMENT '담당자명',
    account_id      VARCHAR(100)    NOT NULL COMMENT '소셜 미디어 계정 아이디',
    is_active       TINYINT(1)      NOT NULL DEFAULT 1 COMMENT '활성화 상태 (1: 활성, 0: 비활성)',
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (assignee_id),
    CONSTRAINT fk_ba_brand    FOREIGN KEY (brand_id)    REFERENCES brand (brand_id)           ON DELETE CASCADE,
    CONSTRAINT fk_ba_platform FOREIGN KEY (platform_id) REFERENCES social_platform (platform_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='브랜드 담당자 정보';

-- ⑤ 소셜 미디어 게시물 수집
CREATE TABLE IF NOT EXISTS social_post_crawl (
    spc_id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    -- 수집 메타
    platform_id      VARCHAR(50)     NOT NULL COMMENT 'social_platform.platform_id 참조',
    crawl_case       VARCHAR(10)     NOT NULL COMMENT '수집 유형 (CASE1: 공식계정, CASE2: 키워드검색)',
    brand_name       VARCHAR(100)    NOT NULL COMMENT '브랜드명',
    account_id       VARCHAR(200)    NOT NULL COMMENT '계정 ID/핸들',
    account_type     VARCHAR(10)     NOT NULL COMMENT '계정 유형 (brand_social_channel.region 참조: KR, HQ 등)',
    -- 게시물 정보
    post_id          VARCHAR(200)    NOT NULL COMMENT '게시물 고유 ID',
    post_url         VARCHAR(500)    NOT NULL COMMENT '게시물 원본 URL',
    post_type        VARCHAR(30)     NULL     COMMENT '게시물 유형 (릴스, 피드, 쇼츠, 영상, 트윗 등)',
    posted_at        DATETIME        NOT NULL COMMENT '게시 일시',
    post_title       VARCHAR(255)    NULL     COMMENT '게시물 제목',
    text_content     TEXT            NULL     COMMENT '게시물 텍스트/캡션',
    person_tags      TEXT            NULL     COMMENT '인물태그 목록 (JSON array)',
    hashtags         TEXT            NULL     COMMENT '해시태그 목록 (JSON array)',
    media_url        TEXT            NULL     COMMENT '미디어(이미지/영상) URL (첫 번째 미디어, CDN signed URL로 장문 가능)',
    thumbnail_url    TEXT            NULL     COMMENT '썸네일 이미지 URL (image_versions2 최소 크기)',
    -- 통계
    view_count       BIGINT          NULL     COMMENT '조회수',
    like_count       BIGINT          NULL     COMMENT '좋아요 수',
    comment_count    BIGINT          NULL     COMMENT '댓글 수',
    share_count      BIGINT          NULL     COMMENT '공유/리트윗 수',
    -- CASE2 전용
    matched_keywords TEXT            NULL     COMMENT '매칭된 키워드 목록 (JSON array, CASE2 전용)',
    author_name      VARCHAR(200)    NULL     COMMENT '작성자명 (CASE2: 인플루언서명)',
    author_followers BIGINT          NULL     COMMENT '작성자 팔로워 수',
    -- 플래그 & 원본
    is_duplicate     TINYINT(1)      NOT NULL DEFAULT 0 COMMENT '중복 여부 (0: 정상, 1: 중복)',
    is_junk          TINYINT(1)      NOT NULL DEFAULT 0 COMMENT '정크 여부 (0: 정상, 1: 정크)',
    raw_data         JSON            NULL     COMMENT 'API 원본 응답 데이터 (재처리 대비 원본 보존)',
    -- 타임스탬프
    created_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP             COMMENT '수집 일시',
    updated_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정 일시',
    PRIMARY KEY (spc_id),
    UNIQUE KEY uq_platform_post   (platform_id, post_id),
    INDEX idx_brand_platform      (brand_name, platform_id),
    INDEX idx_crawl_case          (crawl_case),
    INDEX idx_posted_at           (posted_at),
    INDEX idx_is_duplicate        (is_duplicate),
    INDEX idx_is_junk             (is_junk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='소셜 미디어 브랜드 크롤링 수집 데이터';

-- ⑥ 크롤링용 로그인 계정
CREATE TABLE IF NOT EXISTS social_crawl_account (
    account_id      BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name            VARCHAR(100)    NOT NULL COMMENT '계정 이름 (담당자명 또는 계정 별칭)',
    platform_id     VARCHAR(50)     NOT NULL COMMENT 'social_platform.platform_id 참조',
    login_id        VARCHAR(200)    NOT NULL COMMENT '로그인 ID (암호화 저장 권장)',
    login_pw        VARCHAR(500)    NOT NULL COMMENT '로그인 비밀번호 (AES-256 암호화 필수)',
    issue           TEXT            NULL     COMMENT '이슈 사항 (차단, 세션 만료, 2FA 등)',
    status          VARCHAR(20)     NOT NULL DEFAULT 'ACTIVE' COMMENT '계정 상태 (ACTIVE, BLOCKED, EXPIRED, PAUSED)',
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (account_id),
    UNIQUE KEY uq_platform_login_id (platform_id, login_id),
    INDEX idx_platform_id (platform_id),
    INDEX idx_status      (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='소셜 미디어 크롤링용 로그인 계정 관리';

-- ⑦ 수집 필터 키워드 (정크 / CASE2)
CREATE TABLE IF NOT EXISTS social_crawl_exclude_keyword (
    keyword_id      BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    keyword_type    VARCHAR(20)     NOT NULL COMMENT '키워드 유형 (JUNK, CASE2_FILTER)',
    platform_id     VARCHAR(50)     NOT NULL COMMENT 'social_platform.platform_id 참조',
    brand_id        BIGINT UNSIGNED NULL     DEFAULT NULL COMMENT '적용 브랜드 ID (NULL: 전체 공통)',
    filter_keyword  VARCHAR(500)    NULL     COMMENT 'CASE2 수집 필터 키워드 (keyword_type=CASE2_FILTER 시 사용)',
    junk_keyword    VARCHAR(500)    NULL     COMMENT '정크 필터 키워드 (keyword_type=JUNK 시 사용)',
    match_type      VARCHAR(20)     NOT NULL DEFAULT 'CONTAINS' COMMENT '매칭 방식 (CONTAINS, EXACT, REGEX)',
    description     VARCHAR(300)    NULL     DEFAULT NULL COMMENT '등록 사유 / 설명',
    is_active       TINYINT(1)      NOT NULL DEFAULT 1 COMMENT '활성화 여부 (0: 비활성, 1: 활성)',
    created_by      VARCHAR(100)    NULL     DEFAULT NULL COMMENT '등록자',
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (keyword_id),
    INDEX idx_keyword_type (keyword_type),
    INDEX idx_platform_id  (platform_id),
    INDEX idx_brand_id     (brand_id),
    INDEX idx_is_active    (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='소셜 미디어 크롤링 필터링 키워드 관리 (정크 / CASE2 수집 필터)';
