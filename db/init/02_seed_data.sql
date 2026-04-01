-- ============================================================
-- 초기 데이터 (Seed)
-- INSERT IGNORE: 이미 존재하는 행은 건너뜀 (데이터 없을 때만 삽입)
-- ============================================================

SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
SET CHARACTER SET utf8mb4;
SET character_set_connection = utf8mb4;

INSERT IGNORE INTO social_platform (platform_id, platform_name) VALUES ('instagram', '인스타그램');

-- 브랜드
INSERT IGNORE INTO brand (brand_id, brand_name) VALUES
    (1, 'Instagram'),
    (2, 'MUSINSA');

-- 브랜드 SNS 채널
INSERT IGNORE INTO brand_social_channel (brand_id, platform_id, region, channel_url) VALUES
    (1, 'instagram', 'HQ', 'https://www.instagram.com/instagram'),
    (2, 'instagram', 'KR', 'https://www.instagram.com/musinsa.official/');

-- 브랜드 담당자 (크롤링 대상 계정)
INSERT IGNORE INTO brand_assignee (brand_id, platform_id, assignee_name, account_id, is_active) VALUES
    (1, 'instagram', '테스터', 'instagram',        1),
    (2, 'instagram', '테스터', 'musinsa.official', 1);