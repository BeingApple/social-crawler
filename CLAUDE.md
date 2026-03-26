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

> **분석 일시**: 2026-03-26 | **분석 유형**: 실제 구현 기반

### 디렉토리 구조

```
brand-social-crawler/
├── docker-compose.yml              # 4개 서비스 통합 오케스트레이션
├── .env.example                    # 환경변수 템플릿
│
├── db/init/
│   └── 01_schema.sql              # 자동 실행 DDL (brand, post 테이블 + 샘플 데이터)
│
├── crawler/                        # Python 배치 서버
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
│       ├── db.py                  # SQLAlchemy 엔진/세션 (SessionLocal, Base)
│       ├── models.py              # Brand, Post ORM 모델
│       ├── crawler.py             # Playwright + BeautifulSoup 크롤러 + 더미 Insert
│       └── main.py                # schedule 라이브러리 기반 주기 실행 엔트리포인트
│
├── backend/                        # Spring Boot 어드민 REST API
│   ├── Dockerfile                 # 멀티스테이지 (JDK build → JRE runtime)
│   ├── build.gradle               # Java 21, Spring Boot 3.3
│   └── src/main/
│       ├── java/com/musinsa/crawler/
│       │   ├── CrawlerApplication.java
│       │   ├── domain/entity/Post.java
│       │   ├── domain/repository/PostRepository.java
│       │   ├── api/controller/PostController.java   # GET /api/posts, /api/posts/{id}
│       │   └── api/dto/PostResponse.java
│       └── resources/application.yml               # DB 연결, JPA, CORS 설정
│
└── frontend/                       # React + TypeScript + Vite + MUI 어드민 대시보드
    ├── Dockerfile                  # Vite build → nginx 서빙
    ├── nginx.conf                  # SPA 라우팅 + /api 리버스 프록시
    ├── vite.config.ts              # 개발 서버 프록시 설정
    ├── tsconfig.json               # TS 프로젝트 참조 루트
    ├── tsconfig.app.json           # src/ 대상, strict: true
    ├── tsconfig.node.json          # vite.config.ts 전용
    └── src/
        ├── main.tsx               # MUI ThemeProvider + BrowserRouter
        ├── App.tsx                # AppBar + Routes
        ├── types/post.ts          # Post, PageResponse<T>, FetchPostsParams 인터페이스
        ├── api/posts.ts           # axios 기반 타입 안전 API 클라이언트
        └── pages/PostListPage.tsx # MUI DataGrid, 플랫폼 필터, 서버사이드 페이징
```

### 실제 DB 스키마

```sql
-- brand: 플랫폼별 계정 단위 (brand_name + platform + account_handle 복합 Unique)
brand_id, brand_name, platform, account_handle, is_active, created_at, updated_at

-- post: 수집된 게시물 원본 (platform + external_post_id Unique)
post_id, brand_id, platform, external_post_id,
content, media_urls(JSON), hashtags(JSON),
likes, comments, shares, views,
posted_at, crawled_at
```

### API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| GET | `/api/posts` | 게시물 목록 (페이징, ?platform 필터) |
| GET | `/api/posts/{id}` | 게시물 단건 조회 |

### 환경 변수 (docker-compose 주입)

| 변수 | 용도 |
|------|------|
| `MYSQL_*` | DB 접속 정보 |
| `CRAWL_INTERVAL_SEC` | 크롤 주기(초), 기본 3600 |
| `VITE_API_BASE_URL` | 프론트 → 백엔드 API URL |
| `SPRING_DATASOURCE_*` | Spring Boot DB 연결 |

### 실행 방법

```bash
cp .env.example .env
docker-compose up --build
# Admin UI  → http://localhost:3000
# REST API  → http://localhost:8080/api/posts
```

### 중복 방지 전략

- DB: `UNIQUE KEY uq_platform_post (platform, external_post_id)`
- Python ORM: Insert 전 `filter_by(platform, external_post_id).first()` 체크
