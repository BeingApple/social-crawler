# brand-social-crawler — Claude 컨텍스트

> Jira: MZMSS-31 | 클레임개발팀-운영효율화

## 프로젝트 개요

무신사 입점 브랜드의 소셜 미디어 데이터를 **매일 전날 기준**으로 수집하고, AI 요약 후 Slack으로 알림을 제공하는 크롤링 파이프라인.

## 수집 대상

| 플랫폼 | 수집 유형 |
|--------|-----------|
| Instagram | 릴스 (Reels) |
| TikTok | 영상 게시물 |
| X (Twitter) | 게시물 (트윗) |

- 브랜드 공식 계정 + 검색어 기반 병행 수집
- 후처리: 정크 키워드 필터링 + 중복 제거
- 모든 원본 데이터 DB 저장

## 시스템 흐름

```
[SNS 플랫폼] → [Crawler (Python)] → [MySQL DB]
                                          │
                              ┌───────────┴───────────┐
                              ▼                       ▼
                   Spring Boot REST API        (예정) Claude 요약
                              │                       │
                              ▼                       ▼
                   React Admin Dashboard      Slack 알림
```

### 컨테이너 통신 구조 (docker-compose)
```
crawler ──write──► db:3306
backend ──read───► db:3306
frontend :3000 ──/api/*──► backend:8080
```

## 인프라

- 서버: dev EC2 (무신사 내부)
- DB: dev DB (무신사 내부)
- Slack Hook / Claude Hook: 무신사 제공

## 기술 스택 (구현 완료)

| 모듈 | 스택 |
|------|------|
| **Crawler** | Python 3.11, Playwright, BeautifulSoup4, SQLAlchemy 2.0, schedule |
| **Backend** | Java 21, Spring Boot 3.3, Spring Data JPA, Lombok |
| **Frontend** | React 18, **TypeScript 5.5**, Vite 5, MUI v5, MUI X DataGrid, React Router v6, axios |
| **DB** | MySQL 8.0 (Aurora MySQL 8.0 호환) |
| **인프라** | Docker Compose, nginx (프론트 서빙 + API 프록시) |

## 핵심 데이터 모델 (설계 기준)

```sql
-- 브랜드
brand_id, brand_name, musinsa_brand_code,
instagram_handle, tiktok_username, twitter_handle,
created_at, updated_at, is_active

-- 게시물 원본
post_id, brand_id, platform, external_post_id,
content, media_urls, hashtags,
likes, comments, shares, views,
posted_at, crawled_at

-- 소셜 지표 (시계열)
brand_id, platform, metric_type, metric_value,
collected_at, period
```

## 주요 제약사항

- 로그인 필요 플랫폼은 크롤링 불가할 수 있음
- 각 플랫폼 robots.txt 및 ToS 준수 필수
- API rate limit 대응 로직 필수
  - Instagram Graph API: 200 요청/시간
  - YouTube Data API: 10,000 유닛/일
- 공개 비즈니스 계정 데이터만 수집 (개인정보보호법 PIPA)
- 중복 수집 방지: Redis SET + DB unique constraint

## 사전 준비 필요 항목

- [ ] 플랫폼별 브랜드 공식 계정 목록
- [ ] 크롤링 대상 컬럼 정의
- [ ] 기존 뉴스 크롤링 스크립트 공유

---

## Project Analysis

> **분석 일시**: 2026-03-30 | **분석 유형**: 실제 구현 기반 (전체 코드 정밀 분석)

### 기술 스택

| 모듈 | 스택 | 비고 |
|------|------|------|
| **Crawler** | Python 3.11, Playwright 1.44, httpx 0.27, PyMySQL 1.1, schedule 1.2 | SQLAlchemy ORM은 코드가 주석 처리됨; 실제 DB 접근은 PyMySQL raw cursor |
| **Backend** | Java 21, Spring Boot 3.3.0, Spring Data JPA, HikariCP, Lombok, Validation | Gradle 빌드 |
| **Frontend** | React 18.3, TypeScript 5.5, Vite 8.0, MUI v5 + MUI v7 (icons/system), MUI X DataGrid v7, React Router v6, axios | MUI 버전 혼용 주의 (v5 core + v7 icons/system) |
| **DB** | MySQL 8.0 (Aurora MySQL 8.0 호환) | InnoDB, utf8mb4_unicode_ci |
| **인프라** | Docker Compose (4서비스), nginx (프론트 서빙 + API 프록시), Makefile | |

### 아키텍처 패턴

- **모노레포 멀티모듈**: 단일 리포지토리에 crawler/backend/frontend/db 4개 모듈
- **Crawler**: 레이어드 아키텍처 (social → service → resource → common)
  - `BaseCrawler` ABC 패턴으로 플랫폼별 크롤러 확장 (현재 Instagram만 구현)
  - `CrawlService`가 오케스트레이션: brand 조회 → crawler 실행 → 필터링 → 저장 → 알림
  - Repository 패턴: `BrandRepository`, `SocialPostRepository`, `CrawlJobRepository` (raw PyMySQL)
- **Backend**: Spring 표준 레이어드 (Controller → Repository → Entity)
  - 별도 Service 레이어 없이 Controller에서 직접 Repository 호출
- **Frontend**: 페이지 기반 라우팅 + 샘플 데이터 기반 UI 프로토타입
  - 실제 API 연동: PostListPage만 (axios → `/api/posts`)
  - DashboardPage, CrawlingStatusPage는 하드코딩된 샘플 데이터 사용

### 디렉토리 구조

```
brand-social-crawler/
├── docker-compose.yml              # 4개 서비스 (db, crawler, backend, frontend)
├── Makefile                        # 편의 명령어 (up, down, db, backend, frontend, crawler)
├── .env.example                    # 환경변수 템플릿
│
├── db/init/
│   └── 01_schema.sql              # DDL: brand, post 테이블 + 샘플 브랜드 3건
│
├── crawler/                        # Python 배치 크롤러
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
│       ├── main.py                # 엔트리포인트 (schedule 기반, 현재 테스트 모드)
│       ├── db.py                  # SQLAlchemy 설정 (전체 주석 처리됨, 미사용)
│       ├── models.py              # SQLAlchemy ORM 모델 (전체 주석 처리됨, 미사용)
│       ├── crawler.py             # 레거시 크롤러 (미사용)
│       ├── config/
│       │   └── database.py        # PyMySQL 커넥션 관리 (DatabaseConfig, get_connection, get_db)
│       ├── social/
│       │   ├── base.py            # BaseCrawler ABC (crawl_official_account, crawl_search)
│       │   └── instagram.py       # InstagramCrawler (Playwright 비동기, 로그인/쿠키 세션 관리)
│       ├── service/
│       │   ├── crawl_service.py   # CrawlService (메인 오케스트레이터)
│       │   ├── summary_service.py # ContentFilter + SummaryService (정크 필터, 플랫폼별 Top5 요약)
│       │   └── monitoring_service.py # MonitoringService (로깅)
│       ├── resource/
│       │   └── repository.py      # BrandRepository, SocialPostRepository, CrawlJobRepository
│       ├── common/
│       │   ├── types.py           # BrandTarget, SocialPost 데이터클래스
│       │   ├── utils.py           # yesterday_range, contains_any, random_user_agent
│       │   ├── http.py            # HttpClient (requests + 재시도 + 429 백오프)
│       │   └── exceptions.py      # CrawlError, RateLimitError, NotFoundError, AccessDeniedError
│       └── notifier/
│           └── slack.py           # SlackNotifier (웹훅 기반 요약 전송)
│
├── backend/                        # Spring Boot REST API
│   ├── Dockerfile                 # 멀티스테이지 (JDK build → JRE runtime)
│   ├── build.gradle               # Java 21, Spring Boot 3.3.0
│   └── src/main/
│       ├── java/com/musinsa/crawler/
│       │   ├── CrawlerApplication.java
│       │   ├── domain/entity/Post.java           # JPA Entity (post 테이블)
│       │   ├── domain/repository/PostRepository.java  # JpaRepository + findByPlatform, findByBrandId
│       │   ├── api/controller/PostController.java     # GET /api/posts, GET /api/posts/{id}
│       │   └── api/dto/PostResponse.java              # DTO (from 팩토리 메서드)
│       └── resources/
│           ├── application.yml          # 기본 설정 (환경변수 오버라이드 지원)
│           └── application-local.yml    # 로컬 개발용 프로파일
│
└── frontend/                       # React Admin 대시보드
    ├── Dockerfile                  # Vite build → nginx 서빙
    ├── nginx.conf                  # SPA 라우팅 + /api 리버스 프록시
    ├── package.json
    ├── vite.config.ts
    └── src/
        ├── main.tsx               # ThemeProvider + BrowserRouter
        ├── App.tsx                # LNB 사이드바 + Routes (3개 페이지)
        ├── types/
        │   ├── post.ts            # Post, PageResponse<T>, FetchPostsParams
        │   ├── brand.ts           # BrandAccount, AccountFilters
        │   └── crawling.ts        # CrawlingPost, CrawlingFilters
        ├── api/
        │   └── posts.ts           # axios 기반 API 클라이언트 (fetchPosts, fetchPost)
        ├── components/
        │   └── dashboard/
        │       └── DataTable.tsx   # 계정 리스트 DataGrid 컴포넌트
        ├── data/
        │   ├── sampleData.ts      # 12건 더미 계정 데이터
        │   └── crawlingSampleData.ts  # 더미 크롤링 게시물 데이터
        └── pages/
            ├── DashboardPage.tsx      # 계정 리스트 (샘플 데이터, 필터링)
            ├── CrawlingStatusPage.tsx  # 크롤링 현황 (샘플 데이터, DataGrid)
            └── PostListPage.tsx       # 게시물 목록 (실제 API 연동)
```

### 핵심 컴포넌트 상세

#### Crawler 모듈

| 클래스/파일 | 역할 | 상태 |
|------------|------|------|
| `InstagramCrawler` | Playwright 기반 Instagram 크롤링 (모바일 뷰포트, 로그인/쿠키 세션, 봇감지 우회) | **구현 완료** (초기) |
| `BaseCrawler` | 크롤러 ABC: `crawl_official_account`, `crawl_search`, 중복 제거 `crawl` | 구현 완료 |
| `CrawlService` | 메인 오케스트레이터 (brand 조회 → 크롤 → 필터 → 저장 → 알림) | 스켈레톤 (대부분 주석) |
| `ContentFilter` | 정크 키워드 기반 콘텐츠 필터 | 구현 완료 (미연결) |
| `SummaryService` | 플랫폼별 Top5 게시물 요약 생성 | 구현 완료 (미연결) |
| `SlackNotifier` | Slack 웹훅으로 요약 알림 전송 | 구현 완료 (미연결) |
| `BrandRepository` | brand 테이블 조회 (현재 테스트용 하드코딩 데이터 사용) | 부분 구현 |
| `SocialPostRepository` | post UPSERT (ON DUPLICATE KEY UPDATE) | 구현 완료 (미연결) |
| `CrawlJobRepository` | crawl_jobs 테이블 관리 (DDL 미존재) | 구현 완료 (미연결) |
| `DatabaseConfig` | PyMySQL 커넥션 관리 (싱글턴 설정, 컨텍스트 매니저) | 구현 완료 |
| `HttpClient` | requests 기반 HTTP (재시도 3회, 429 지수 백오프) | 구현 완료 (미사용) |

#### Frontend 라우팅

| Path | 페이지 | 데이터 소스 |
|------|--------|------------|
| `/` | `/accounts`로 리다이렉트 | - |
| `/accounts` | DashboardPage (계정 리스트) | 샘플 데이터 (하드코딩) |
| `/crawling` | CrawlingStatusPage (크롤링 현황) | 샘플 데이터 (하드코딩) |
| `/dummy` | PostListPage (게시물 목록) | 실제 API (`/api/posts`) |

### 실제 DB 스키마

```sql
-- brand: 플랫폼별 계정 단위
-- UNIQUE KEY uq_brand_platform_handle (brand_name, platform, account_handle)
brand_id BIGINT PK AUTO_INCREMENT,
brand_name VARCHAR(100) NOT NULL,
platform VARCHAR(30) NOT NULL,        -- 'instagram' | 'tiktok' | 'twitter'
account_handle VARCHAR(100) NOT NULL,
is_active TINYINT(1) DEFAULT 1,
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE

-- post: 수집된 게시물 원본
-- UNIQUE KEY uq_platform_post (platform, external_post_id)
-- FK: brand_id → brand(brand_id)
post_id BIGINT PK AUTO_INCREMENT,
brand_id BIGINT NOT NULL,
platform VARCHAR(30) NOT NULL,
external_post_id VARCHAR(200) NOT NULL,
content TEXT,
media_urls JSON,
hashtags JSON,
likes INT DEFAULT 0,
comments INT DEFAULT 0,
shares INT DEFAULT 0,
views BIGINT DEFAULT 0,
posted_at DATETIME,
crawled_at DATETIME DEFAULT CURRENT_TIMESTAMP
```

**참고**: `CrawlJobRepository`가 참조하는 `crawl_jobs` 테이블은 DDL에 미정의 (향후 추가 필요)

### API 엔드포인트

| Method | Path | 파라미터 | 설명 |
|--------|------|---------|------|
| GET | `/api/posts` | `?platform=`, `?page=`, `?size=20`, `?sort=crawledAt,desc` | 게시물 목록 (Spring Page 응답) |
| GET | `/api/posts/{postId}` | - | 게시물 단건 조회 (404 시 empty) |

### 환경 변수

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
| `SLACK_WEBHOOK_URL` | Slack 알림 웹훅 | 없음 (선택) |

### 실행 방법

```bash
# Docker 전체 실행
cp .env.example .env
make up                     # 또는 docker-compose up --build

# 로컬 개발 (모듈별 실행)
make db                     # DB만 Docker로 기동
make backend                # Spring Boot 로컬 실행 (local 프로파일)
make frontend               # React 개발 서버 (localhost:3000)
make setup-python && make crawler  # Python 크롤러 로컬 실행

# 접속
# Admin UI  → http://localhost:3000
# REST API  → http://localhost:8080/api/posts
```

### 중복 방지 전략

- DB: `UNIQUE KEY uq_platform_post (platform, external_post_id)`
- Python Repository: `SocialPostRepository.save()` → `INSERT ... ON DUPLICATE KEY UPDATE`
- Python Repository: `SocialPostRepository.exists()` → 저장 전 존재 여부 확인
- Crawler: `BaseCrawler.crawl()` → `deduped dict` 로 동일 세션 내 중복 제거

### 주요 패턴 및 컨벤션

- **Crawler DB 접근**: SQLAlchemy가 코드에 존재하나 전체 주석 처리됨. 실제로는 PyMySQL raw cursor 사용
- **Instagram 크롤링**: Playwright async → `asyncio.run()` 동기 래퍼 패턴
- **봇 감지 우회**: 모바일 뷰포트(iPhone 14 Pro Max), webdriver 프로퍼티 오버라이드, User-Agent 로테이션, 랜덤 딜레이
- **세션 관리**: Playwright storage_state를 파일로 저장/복원 (`instagram_storage.json`)
- **Backend**: Service 레이어 없이 Controller → Repository 직접 호출 (현재 읽기 전용이므로 적절)
- **Frontend**: LNB(좌측 네비게이션 바) + 헤더 + 메인 콘텐츠 레이아웃

### 개발 진행 상태 및 잠재적 이슈

1. **Crawler 테스트 모드**: `main.py`가 `run_all_test()`를 호출 (DB 연결 없이 하드코딩 데이터 사용). `CrawlService.run()`에서 저장/필터/알림 로직 대부분 주석 처리
2. **SQLAlchemy vs PyMySQL 이중 구조**: `db.py` + `models.py` (SQLAlchemy, 전체 주석)와 `config/database.py` + `resource/repository.py` (PyMySQL raw)가 공존. 정리 필요
3. **crawl_jobs 테이블 미존재**: `CrawlJobRepository`가 참조하나 DDL 미정의
4. **social_posts vs post 테이블명 불일치**: Repository SQL은 `social_posts` 참조, DDL은 `post` 테이블. Backend Entity도 `post` 매핑
5. **MUI 버전 혼용**: package.json에 MUI v5 core + MUI v7 icons/system 혼용 (호환성 이슈 가능)
6. **Frontend 샘플 데이터 의존**: DashboardPage, CrawlingStatusPage가 하드코딩 데이터 사용. 실제 API 연동 미완
7. **Instagram crawl_search()**: `return None` 하드코딩 (미구현)
8. **TikTok/Twitter 크롤러**: 미구현 (crawler_map에 주석 처리)
9. **yesterday_range() 테스트 하드코딩**: 10일 전 ~ 어제로 설정됨 (운영 시 수정 필요)
10. **CrawlJobRepository.finish()**: `finished_at` 컬럼 SET 절 중복
