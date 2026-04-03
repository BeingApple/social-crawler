# brand-social-crawler

브랜드의 소셜 미디어 데이터를 수집하고, AI 요약 후 Slack으로 알림을 제공하는 크롤링 파이프라인.

---

## 프로젝트 구조

```
brand-social-crawler/
├── crawler/          # Python 배치 크롤러 (Playwright + SQLAlchemy)
├── backend/          # Spring Boot REST API (Java 21)
├── frontend/         # React + TypeScript 어드민 대시보드 (Vite + MUI)
├── db/init/          # MySQL 초기 DDL (자동 실행)
├── docker-compose.yml
└── .env.example
```

### 서비스 구성

| 서비스 | 기술 스택 | 포트 | 설명 |
|--------|-----------|------|------|
| `db` | MySQL 8.0 | 3306 | Aurora MySQL 8.0 호환 |
| `crawler` | Python 3.11, Playwright | — | 주기적 크롤링 배치 |
| `backend` | Java 21, Spring Boot 3.3 | 8080 | 어드민 REST API |
| `frontend` | React 18, TypeScript, Vite | 3000 | 어드민 대시보드 |

### 컨테이너 통신

```
crawler ──write──► db:3306
backend ──read───► db:3306
frontend :3000 ──/api/*──► backend:8080
```

---

## 실행 방법

### 사전 준비

```bash
cp .env.example .env
```

### 방법 1 — 전체 Docker 실행 (배포/검증)

```bash
docker compose up --build
```

| URL | 설명 |
|-----|------|
| http://localhost:3000 | 어드민 대시보드 |
| http://localhost:8080/api/posts | REST API |

### 방법 2 — 로컬 개발 (프론트/백엔드 핫리로드)

DB와 크롤러만 Docker로 띄우고, 백엔드·프론트는 로컬에서 실행한다.

**① DB + 크롤러 Docker 실행**
```bash
docker compose up db crawler
```

**② Spring Boot 로컬 실행** (IntelliJ: `Backend: CrawlerApplication`)
```bash
cd backend
./gradlew bootRun
```

**③ 프론트 로컬 실행** (IntelliJ: `Frontend: dev`)
```bash
cd frontend
npm install
npm run dev
```

> 프론트 `/api/*` 요청은 Vite 프록시를 통해 `localhost:8080`으로 자동 전달된다.

---

## IntelliJ 실행 구성

프로젝트를 IntelliJ에서 열면 아래 실행 구성이 자동으로 등록된다.

| 구성명 | 설명 |
|--------|------|
| `Docker: Full Stack` | 전체 4개 서비스 Docker 실행 |
| `Docker: DB & Crawler` | DB + 크롤러만 Docker 실행 |
| `Docker: DB only` | DB만 Docker 실행 (백엔드/크롤러 로컬 개발용) |
| `Backend: CrawlerApplication` | Spring Boot 로컬 실행 (localhost:3306 연결) |
| `Frontend: dev` | Vite 로컬 개발 서버 실행 |
| `Crawler: main` | Python 크롤러 로컬 실행 |

> **IntelliJ Gradle import**: `backend/build.gradle` 우클릭 → **Link Gradle Project**

---

## 환경 변수

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `MYSQL_ROOT_PASSWORD` | `root1234` | MySQL root 비밀번호 |
| `MYSQL_DATABASE` | `crawlerdb` | DB명 |
| `MYSQL_USER` | `crawler` | DB 사용자 |
| `MYSQL_PASSWORD` | `crawler1234` | DB 비밀번호 |
| `CRAWL_INTERVAL_SEC` | `3600` | 크롤링 주기 (초) |
| `VITE_API_BASE_URL` | `http://localhost:8080` | 프론트 API 엔드포인트 |

---

## DB 스키마

초기 스키마는 `db/init/01_schema.sql`에서 관리하며, Docker 컨테이너 최초 실행 시 자동 적용된다.

```sql
-- brand: 플랫폼별 계정 단위
brand_id, brand_name, platform, account_handle, is_active, created_at, updated_at

-- post: 수집된 게시물 원본
post_id, brand_id, platform, external_post_id,
content, media_urls(JSON), hashtags(JSON),
likes, comments, shares, views,
posted_at, crawled_at
```

---

## 수집 대상 및 방식

**플랫폼 우선순위**

| 우선순위 | 플랫폼 | 수집 대상 |
|----------|--------|-----------|
| 1차 | Instagram | 피드, 릴스, 스토리 |
| 1차 | YouTube | 영상, 쇼츠 |
| 2차 | X (Twitter) | 트윗 |
| 2차 | TikTok | 영상 |

**크롤링 CASE**

- **CASE 1**: 브랜드 공식 계정(KR + HQ) 게시글 전체 수집
- **CASE 2**: 브랜드명 키워드 검색 → 광고/프로모션 키워드 필터링 (인플루언서 광고 포착)

---

## 주요 제약사항

- 로그인 필요 플랫폼은 크롤링 불가할 수 있음
- 각 플랫폼 ToS 및 robots.txt 준수 필수
- 공개 비즈니스 계정 데이터만 수집 (개인정보보호법 PIPA)
- 중복 수집 방지: `platform + external_post_id` 기준 unique constraint

---

