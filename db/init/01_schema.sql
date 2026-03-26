-- ============================================================
-- brand-social-crawler 초기 스키마 (DRAFT)
-- Aurora MySQL 8.0 호환
--
-- ⚠️  이 파일은 개발 시작을 위한 임시 초안입니다.
--     정식 스키마 확정 전까지 자유롭게 수정하세요.
--     확정 후 flyway 또는 liquibase 마이그레이션으로 전환 예정.
-- ============================================================

CREATE TABLE IF NOT EXISTS brand (
    brand_id        BIGINT          NOT NULL AUTO_INCREMENT,
    brand_name      VARCHAR(100)    NOT NULL,
    platform        VARCHAR(30)     NOT NULL COMMENT 'instagram | tiktok | twitter',
    account_handle  VARCHAR(100)    NOT NULL COMMENT '크롤링 대상 계정 핸들',
    is_active       TINYINT(1)      NOT NULL DEFAULT 1,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (brand_id),
    UNIQUE KEY uq_brand_platform_handle (brand_name, platform, account_handle)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS post (
    post_id          BIGINT          NOT NULL AUTO_INCREMENT,
    brand_id         BIGINT          NOT NULL,
    platform         VARCHAR(30)     NOT NULL,
    external_post_id VARCHAR(200)    NOT NULL COMMENT '플랫폼 원본 게시물 ID',
    content          TEXT,
    media_urls       JSON,
    hashtags         JSON,
    likes            INT             NOT NULL DEFAULT 0,
    comments         INT             NOT NULL DEFAULT 0,
    shares           INT             NOT NULL DEFAULT 0,
    views            BIGINT          NOT NULL DEFAULT 0,
    posted_at        DATETIME,
    crawled_at       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (post_id),
    UNIQUE KEY uq_platform_post (platform, external_post_id),
    CONSTRAINT fk_post_brand FOREIGN KEY (brand_id) REFERENCES brand (brand_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 샘플 브랜드 데이터
INSERT IGNORE INTO brand (brand_name, platform, account_handle) VALUES
    ('MUSINSA', 'instagram', 'musinsa_official'),
    ('MUSINSA', 'tiktok',    'musinsa_official'),
    ('MUSINSA', 'twitter',   'musinsa');
