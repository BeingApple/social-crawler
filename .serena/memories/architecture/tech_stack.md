# brand-social-crawler - 실제 기술 스택

**분석 일시**: 2026-03-26
**유형**: 실제 구현 기반

## Crawler (Python)

| 항목 | 버전/선택 |
|------|----------|
| Python | 3.11 (Dockerfile: `python:3.11-slim`) |
| 크롤링 | Playwright 1.44.0 (Chromium headless), BeautifulSoup4 4.12.3 |
| HTTP | httpx 0.27.0 |
| ORM | SQLAlchemy 2.0.30 (`mapped_column` 스타일) |
| DB 드라이버 | PyMySQL 1.1.1 + cryptography 42.x |
| 스케줄러 | schedule 1.2.2 (`CRAWL_INTERVAL_SEC` 환경변수로 주기 조절) |
| 환경변수 | python-dotenv 1.0.1 |

## Backend (Java)

| 항목 | 버전/선택 |
|------|----------|
| Java | 21 (eclipse-temurin:21) |
| Framework | Spring Boot 3.3.0 |
| ORM | Spring Data JPA + Hibernate |
| DB 드라이버 | `com.mysql:mysql-connector-j` |
| 편의 | Lombok (getter, builder, RequiredArgsConstructor) |
| 빌드 | Gradle 8.x (gradlew wrapper 포함) |
| Dockerfile | 멀티스테이지: JDK 빌드 → JRE 런타임 |

## Frontend (TypeScript)

| 항목 | 버전/선택 |
|------|----------|
| 언어 | **TypeScript 5.5** (`strict: true`, `noUnusedLocals/Parameters`) |
| Framework | React 18.3 |
| 빌드 도구 | Vite 5.3 (`vite.config.ts`) |
| UI 라이브러리 | MUI v5 (Material UI) + `@mui/x-data-grid` v7 |
| 라우팅 | React Router v6 |
| HTTP 클라이언트 | axios 1.7 (제네릭 타입 적용) |
| 서빙 | nginx:alpine (SPA 라우팅 + `resolver 127.0.0.11` 동적 프록시) |
| TS 설정 | `tsconfig.json` (루트) → `tsconfig.app.json` (src) + `tsconfig.node.json` (vite) |

## Database

| 항목 | 선택 |
|------|------|
| 엔진 | MySQL 8.0 (`mysql:8.0` 이미지, Aurora MySQL 8.0 호환) |
| 초기화 | `db/init/01_schema.sql` 자동 실행 |
| 스키마 관리 | `ddl-auto: none` — SQL 파일로 직접 관리 |
| JSON 컬럼 | `media_urls`, `hashtags` — MySQL JSON 타입 |

## 인프라

| 항목 | 선택 |
|------|------|
| 오케스트레이션 | Docker Compose (`version: "3.9"`) |
| 데이터 보존 | Named volume `db_data` |
| 헬스체크 | `mysqladmin ping` → crawler/backend `depends_on condition: service_healthy` |
| 개발 핫리로드 | crawler 소스 volume mount (`./crawler/src:/app/src`) |
