# DB Patterns (2026-03-30)

## 테이블
- brand: brand_id(PK), brand_name, platform, account_handle, is_active, created_at, updated_at
  - UNIQUE: (brand_name, platform, account_handle)
- post: post_id(PK), brand_id(FK->brand), platform, external_post_id, content, media_urls(JSON), hashtags(JSON), likes, comments, shares, views, posted_at, crawled_at
  - UNIQUE: (platform, external_post_id)
- crawl_jobs: Repository 코드 존재하나 DDL 미정의 (추가 필요)

## 접근 패턴
- Crawler(write): PyMySQL raw cursor, 수동 commit, INSERT ON DUPLICATE KEY UPDATE
- Backend(read): Spring Data JPA, HikariCP pool(max 10), findByPlatform/findByBrandId

## 이슈
- Crawler Repository가 social_posts 테이블 참조하나 실제 DDL은 post
- SQLAlchemy ORM 코드(db.py, models.py) 전체 주석처리됨