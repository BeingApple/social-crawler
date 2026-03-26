# brand-social-crawler - 실제 데이터 아키텍처 패턴

**분석 일시**: 2026-03-26

## 실제 데이터 흐름

```
[SNS 플랫폼]
    │
    ▼
[crawler-python]
    │  Playwright 렌더링 → BS4 파싱
    │  중복 체크(ORM) → INSERT
    ▼
[crawler-db:3306 / MySQL 8.0]
    │
    ▼
[crawler-backend:8080]
    │  Spring Data JPA → Pageable 조회
    ▼
[crawler-frontend:3000]
    │  axios GET /api/posts → MUI DataGrid
    ▼
[사용자 브라우저]
```

## 실제 스키마

### brand 테이블
```sql
CREATE TABLE brand (
    brand_id       BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    brand_name     VARCHAR(100) NOT NULL,
    platform       VARCHAR(30)  NOT NULL,  -- instagram | tiktok | twitter
    account_handle VARCHAR(100) NOT NULL,
    is_active      TINYINT(1)   DEFAULT 1,
    created_at     DATETIME     DEFAULT CURRENT_TIMESTAMP,
    updated_at     DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_brand_platform_handle (brand_name, platform, account_handle)
);
```

### post 테이블
```sql
CREATE TABLE post (
    post_id          BIGINT       NOT NULL AUTO_INCREMENT PRIMARY KEY,
    brand_id         BIGINT       NOT NULL,
    platform         VARCHAR(30)  NOT NULL,
    external_post_id VARCHAR(200) NOT NULL,
    content          TEXT,
    media_urls       JSON,
    hashtags         JSON,
    likes            INT          DEFAULT 0,
    comments         INT          DEFAULT 0,
    shares           INT          DEFAULT 0,
    views            BIGINT       DEFAULT 0,
    posted_at        DATETIME,
    crawled_at       DATETIME     DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_platform_post (platform, external_post_id),
    FOREIGN KEY (brand_id) REFERENCES brand(brand_id)
);
```

## 중복 수집 방지 (이중 가드)

| 레이어 | 방법 |
|--------|------|
| DB | `UNIQUE KEY (platform, external_post_id)` — MySQL에서 중복 Insert 거부 |
| Application | Python ORM `filter_by(platform=, external_post_id=).first()` 후 신규만 Insert |

> Redis SET 방식은 현재 미구현. 향후 대용량 처리 시 추가 권장.

## SQLAlchemy 패턴 (Crawler)

```python
# 세션 사용 패턴 (with 컨텍스트 매니저)
with SessionLocal() as session:
    obj = session.query(Post).filter_by(...).first()
    if not obj:
        session.add(Post(**row))
    session.commit()
```

## JPA 패턴 (Backend)

```java
// 서버사이드 페이징
Page<Post> page = postRepository.findByPlatform(platform, pageable);
return page.map(PostResponse::from);

// DTO 변환: static factory
PostResponse.from(post)  // Builder 패턴
```

## DDL 관리 전략

- **초기화**: `db/init/01_schema.sql` → MySQL 컨테이너 최초 기동 시 자동 실행
- **마이그레이션**: `ddl-auto: none` (Spring Boot) — 스키마 변경은 SQL 파일로만 관리
- **샘플 데이터**: `01_schema.sql` 하단 `INSERT IGNORE` 3개 브랜드 포함

## JSON 컬럼 처리

- **MySQL**: `media_urls JSON`, `hashtags JSON` 컬럼 타입
- **Python ORM**: `mapped_column(JSON)` → list 자동 직렬화/역직렬화
- **Java JPA**: `@JdbcTypeCode(SqlTypes.JSON)` + `List<String>` 타입 매핑
