# Project Analysis

> **분석 일시**: 2026-03-30 | **분석 유형**: 실제 구현 기반 (전체 코드 정밀 분석)

## 기술 스택

| 모듈 | 스택 | 비고 |
|------|------|------|
| **Crawler** | Python 3.11, Playwright 1.44, httpx 0.27, PyMySQL 1.1, schedule 1.2 | SQLAlchemy ORM은 코드가 주석 처리됨; 실제 DB 접근은 PyMySQL raw cursor |
| **Backend** | Java 21, Spring Boot 3.3.0, Spring Data JPA, HikariCP, Lombok, Validation | Gradle 빌드 |
| **Frontend** | React 18.3, TypeScript 5.5, Vite 8.0, MUI v7, MUI X DataGrid v7, React Router v6, axios | |
| **DB** | MySQL 8.0 (Aurora MySQL 8.0 호환) | InnoDB, utf8mb4_unicode_ci |
| **인프라** | Docker Compose (4서비스), nginx (프론트 서빙 + API 프록시), Makefile | |

## 아키텍처 패턴

- **모노레포 멀티모듈**: 단일 리포지토리에 crawler/backend/frontend/db 4개 모듈
- **Crawler**: 레이어드 아키텍처 (social → service → resource → common)
  - `BaseCrawler` ABC 패턴으로 플랫폼별 크롤러 확장 (현재 Instagram만 구현)
  - `CrawlService`가 오케스트레이션: brand 조회 → crawler 실행 → 필터링 → 저장 → 알림
  - Repository 패턴: `BrandRepository`, `SocialPostRepository`, `CrawlJobRepository` (SQLAlchemy ORM)
- **Backend**: Spring 표준 레이어드 (Controller → Service → Repository → Entity)
  - 신규 코드는 Service 레이어 필수 (기존 일부는 Controller → Repository 직접 호출이나 점진적 개선 대상)
  - QueryDSL 기반 동적 쿼리 (`SocialPostCrawlRepositoryCustom` / `SocialPostCrawlRepositoryImpl`)
- **Frontend**: 페이지 기반 라우팅, 전 페이지 실제 API 연동 완료
  - DashboardPage → `/api/assignees`, CrawlingStatusPage → `/api/posts`, CrawlAccountPage → `/api/crawl-accounts`

## 디렉토리 구조

```
brand-social-crawler/
├── docker-compose.yml              # 4개 서비스 (db, crawler, backend, frontend)
├── Makefile                        # 편의 명령어 (up, down, db, backend, frontend, crawler)
├── .env.example                    # 환경변수 템플릿
│
├── db/init/
│   └── 01_schema.sql              # DDL: 7개 테이블 스키마
│
├── crawler/                        # Python 배치 크롤러
│   └── src/
│       ├── main.py                # 엔트리포인트 (schedule 기반)
│       ├── social/instagram.py    # InstagramCrawler (Playwright 비동기, 로그인/쿠키 세션)
│       ├── service/crawl_service.py  # CrawlService (메인 오케스트레이터)
│       ├── resource/
│       │   ├── db.py              # SQLAlchemy 엔진 + SessionLocal
│       │   ├── models.py          # SQLAlchemy ORM 모델
│       │   └── repository.py      # SocialCrawlAccountRepository, SocialPostCrawlRepository, SocialCrawlExcludeKeywordRepository
│       └── common/types.py        # SocialPost, BrandAssigneeWithBrand, CrawlAccount 데이터클래스
│
├── backend/                        # Spring Boot REST API
│   └── src/main/java/com/crawler/
│       ├── domain/entity/          # JPA 엔티티 (SocialPostCrawl, SocialCrawlAccount, BrandAssignee 등)
│       ├── domain/repository/      # JpaRepository + QueryDSL (SocialPostCrawlRepositoryImpl)
│       ├── service/                # SocialPostCrawlService, SocialCrawlAccountService, AssigneeService
│       ├── api/controller/         # SocialPostCrawlController, SocialCrawlAccountController, AssigneeController
│       └── common/AesEncryptionUtil.java  # AES-256-GCM 암호화
│
└── frontend/src/
    ├── types/                      # post.ts, brand.ts, crawlAccount.ts
    ├── api/                        # axios 기반 API 클라이언트
    └── pages/                      # DashboardPage, CrawlingStatusPage, CrawlAccountPage (PostListPage)
```

## 핵심 컴포넌트 상태

### Crawler 모듈

| 클래스/파일 | 역할 | 상태 |
|------------|------|------|
| `InstagramCrawler` | Playwright 기반 Instagram 크롤링 (모바일 뷰포트, 로그인/쿠키 세션, 봇감지 우회) | **구현 완료** |
| `BaseCrawler` | 크롤러 ABC: `crawl_official_account`, `crawl_search` | 구현 완료 |
| `CrawlService` | 메인 오케스트레이터 (brand 조회 → 크롤 → 필터 → 저장 → 알림) | **구현 완료** (CASE1 저장 flow 완성, Slack 요약은 주석) |
| `ContentFilter` | 정크 키워드 기반 콘텐츠 필터 | 구현 완료 (CrawlService에 연결됨) |
| `SummaryService` | 플랫폼별 Top5 게시물 요약 생성 | 구현 완료 (미연결) |
| `SlackNotifier` | Slack 웹훅으로 요약 알림 전송 | 구현 완료 (미연결) |
| `SocialPostCrawlRepository` | SQLAlchemy INSERT ON DUPLICATE KEY UPDATE | 구현 완료 |

### Frontend 라우팅

| Path | 페이지 | 데이터 소스 |
|------|--------|------------|
| `/` | `/accounts`로 리다이렉트 | - |
| `/accounts` | DashboardPage (계정 리스트) | 실제 API (`/api/assignees`) |
| `/crawling` | CrawlingStatusPage (크롤링 현황) | 실제 API (`/api/posts`) |
| `/crawl-accounts` | CrawlAccountPage (크롤 계정 관리) | 실제 API (`/api/crawl-accounts`) |

## 실제 DB 스키마

| # | 테이블명 | 설명 |
|---|----------|------|
| ① | `social_platform` | SNS 플랫폼 마스터 (instagram, youtube, x, tiktok) |
| ② | `brand` | 브랜드 기본 정보 |
| ③ | `brand_social_channel` | 브랜드 × 플랫폼 × 지역 매핑 (채널 URL) |
| ④ | `brand_assignee` | 브랜드 담당자 및 소셜 계정 ID 관리 |
| ⑤ | `social_post_crawl` | 수집된 게시물 원본 데이터 (메인 적재) |
| ⑥ | `social_crawl_account` | 크롤링용 로그인 계정 (AES-256-GCM 암호화) |
| ⑦ | `social_crawl_exclude_keyword` | 정크/수집 필터 키워드 관리 |

```sql
-- ⑤ social_post_crawl (메인 적재 테이블)
spc_id        BIGINT UNSIGNED  PK AUTO_INCREMENT
platform_id   VARCHAR(50)      FK → social_platform
crawl_case    VARCHAR(10)      -- 'CASE1' | 'CASE2'
brand_name    VARCHAR(100)
account_id    VARCHAR(200)
account_type  VARCHAR(10)      -- brand_social_channel.region (KR, HQ)
post_id       VARCHAR(200)     -- Instagram shortcode 등
post_url      VARCHAR(500)
post_type     VARCHAR(30)      -- '릴스', '피드' 등
posted_at     DATETIME
post_title    VARCHAR(255)
text_content  TEXT
hashtags      TEXT             -- JSON array
person_tags   TEXT             -- JSON array
media_url     TEXT             -- CDN signed URL로 장문 가능
view_count    BIGINT
like_count    BIGINT
comment_count BIGINT
share_count   BIGINT
matched_keywords TEXT          -- JSON array, CASE2 전용
author_name   VARCHAR(200)     -- CASE2 전용
author_followers BIGINT        -- CASE2 전용
is_duplicate  TINYINT(1)
is_junk       TINYINT(1)
raw_data      JSON
UNIQUE KEY uq_platform_post (platform_id, post_id)

-- ⑥ social_crawl_account
account_id   BIGINT UNSIGNED  PK AUTO_INCREMENT
name         VARCHAR(100)
platform_id  VARCHAR(50)      FK → social_platform
login_id     VARCHAR(200)     -- AES-256-GCM 암호화
login_pw     VARCHAR(500)     -- AES-256-GCM 암호화
issue        TEXT
status       VARCHAR(20)      -- 'ACTIVE' | 'BLOCKED' | 'EXPIRED' | 'PAUSED'
UNIQUE KEY uq_platform_login_id (platform_id, login_id)
```

전체 DDL: `db/init/01_schema.sql` 참조

## API 엔드포인트

| Method | Path | 파라미터 | 설명 |
|--------|------|---------|------|
| GET | `/api/posts` | `platformId`, `brandName`, `crawlCase`, `postedFrom`, `postedTo`, `page`, `size`(기본 20) | 게시물 목록 (페이징 + QueryDSL 다중 필터) |
| GET | `/api/posts/{spcId}` | - | 게시물 단건 조회 |
| GET | `/api/assignees` | - | 담당자 목록 조회 |
| GET | `/api/crawl-accounts` | - | 크롤 계정 목록 (loginPw 미포함) |
| GET | `/api/crawl-accounts/{id}` | - | 크롤 계정 단건 조회 (loginPw 미포함) |
| GET | `/api/crawl-accounts/{id}/decrypt` | - | loginId + loginPw 원문 복호화 반환 |
| POST | `/api/crawl-accounts` | `SocialCrawlAccountRequest` | 크롤 계정 생성 (201) |
| PUT | `/api/crawl-accounts/{id}` | `SocialCrawlAccountRequest` | 크롤 계정 수정 |
| DELETE | `/api/crawl-accounts/{id}` | - | 크롤 계정 삭제 (204) |

## 환경 변수

| 변수 | 용도 | 기본값 |
|------|------|--------|
| `MYSQL_ROOT_PASSWORD` | DB root 패스워드 | `root1234` |
| `MYSQL_DATABASE` | DB 이름 | `crawlerdb` |
| `MYSQL_USER` / `MYSQL_PASSWORD` | DB 계정 | `crawler` / `crawler1234` |
| `CRAWL_INTERVAL_SEC` | 크롤 주기(초) | `3600` |
| `VITE_API_BASE_URL` | 프론트 → 백엔드 URL | `http://localhost:8080` |
| `SPRING_DATASOURCE_*` | Spring Boot DB 연결 | docker-compose에서 주입 |
| `SPRING_PROFILES_ACTIVE` | Spring 프로파일 | `local` |
| `INSTAGRAM_USERNAME` / `INSTAGRAM_PASSWORD` | Instagram 로그인 | 없음 (필수) |
| `ENCRYPTION_SECRET_KEY` | AES-256-GCM 암호화 키 | 없음 (필수) |
| `SLACK_WEBHOOK_URL` | Slack 알림 웹훅 | 없음 (선택) |

## 주요 패턴 및 컨벤션

- **Crawler DB 접근**: SQLAlchemy ORM (`resource/db.py` + `resource/models.py` + `resource/repository.py`)
- **Instagram 크롤링**: Playwright async → `asyncio.run()` 동기 래퍼 패턴
- **봇 감지 우회**: 모바일 뷰포트(iPhone 14 Pro Max), webdriver 프로퍼티 오버라이드, User-Agent 로테이션, 랜덤 딜레이
- **세션 관리**: Playwright storage_state를 파일로 저장/복원 (`instagram_storage_{username}.json`, 계정별 분리)
- **Backend**: Controller → Service → Repository 레이어 구조 사용 (신규 코드 기준)
- **DTO**: `from()` 팩토리 메서드 패턴
- **암호화**: AES-256-GCM, `Base64(IV[12B] || CipherText+AuthTag)` 형식
- **중복 방지**: `uq_platform_post (platform_id, post_id)` + `exists()` 체크 + `ON DUPLICATE KEY UPDATE`

## 개발 진행 상태

| 항목 | 상태 |
|------|------|
| Instagram CASE1 (공식 계정 수집) | 구현 완료 |
| Instagram CASE2 (해시태그 검색) | 코드 작성됨, 비활성 |
| DB 저장 연동 | 구현 완료 |
| 정크 키워드 필터링 | 구현 완료 (CrawlService 연결됨) |
| Slack 알림 | 코드 작성됨, 미연결 |
| TikTok / X 크롤러 | 미구현 |
| AI 요약 (Claude) | 미구현 |
| Frontend 실제 API 연동 | 구현 완료 (DashboardPage, CrawlingStatusPage, CrawlAccountPage) |
| 크롤 계정 관리 CRUD | 구현 완료 (Backend API + Frontend CrawlAccountPage) |
