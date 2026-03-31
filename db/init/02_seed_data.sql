-- ============================================================
-- 초기 데이터 (Seed)
-- INSERT IGNORE: 이미 존재하는 행은 건너뜀 (데이터 없을 때만 삽입)
-- ============================================================

INSERT IGNORE INTO social_platform (platform_id, platform_name) VALUES
    ('instagram', '인스타그램'),
    ('youtube',   '유튜브'),
    ('x',         'X (Twitter)'),
    ('tiktok',    '틱톡');