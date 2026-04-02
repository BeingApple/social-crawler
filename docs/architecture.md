# brand-social-crawler 아키텍처 문서

---

## 1. 프로젝트 개요

무신사 입점 브랜드의 소셜 미디어 데이터를 매일 전날 기준으로 수집하고, 정크 필터링·중복 제거 후 DB에 저장하는 크롤링 파이프라인입니다.  
현재 1차 개발 범위는 Instagram(공식 계정 수집)이며, 향후 TikTok / X(Twitter)로 확장 예정입니다.

---

## 2. 시스템 흐름

```
[Instagram] ──► [Crawler (Python)] ──► [MySQL DB]
                                            │
                               ┌────────────┴─────────────┐
                               ▼                          ▼
                    Spring Boot REST API          (예정) Claude AI 요약
                               │                          │
                               ▼                          ▼
                    React Admin Dashboard          Slack 알림 전송
```

크롤러가 DB에 적재 → 백엔드 API가 DB를 읽어 프론트엔드에 제공하는 단방향 파이프라인입니다.

---

## 3. 컨테이너 구성 (docker-compose)

| 서비스 | 이미지/언어 | 포트 | 역할 |
|--------|-------------|------|------|
| db | MySQL 8.0 (Aurora 호환) | 3306 | 데이터 저장소 |
| crawler | Python 3.11 | - | 소셜 데이터 수집 (배치) |
| backend | Java 21 / Spring Boot 3.3 | 8080 | REST API 제공 |
| frontend | React 18 / nginx | 3000 | Admin 대시보드 |

- crawler, backend 모두 `db:3306`에 직접 연결
- frontend는 nginx를 통해 `/api/*` 요청을 `backend:8080`으로 프록시

---

## 4. 기술 스택

| 모듈 | 스택 |
|------|------|
| Crawler | Python 3.11, Playwright 1.44, SQLAlchemy 2.0, schedule 1.2 |
| Backend | Java 21, Spring Boot 3.3, Spring Data JPA, Lombok |
| Frontend | React 18, TypeScript 5.5, Vite 5, MUI v5, MUI X DataGrid, React Router v6, axios |
| DB | MySQL 8.0 (Aurora MySQL 8.0 호환), InnoDB, utf8mb4_unicode_ci |
| Infra | Docker Compose, nginx, Makefile |

---

## 5. DB 스키마 (DDL 기준)

### 테이블 목록

| # | 테이블명 | 설명 |
|---|----------|------|
| ① | social_platform | SNS 플랫폼 마스터 (instagram, youtube, x, tiktok) |
| ② | brand | 브랜드 기본 정보 |
| ③ | brand_social_channel | 브랜드 × 플랫폼 × 지역 매핑 (채널 URL 관리) |
| ④ | brand_assignee | 브랜드 담당자 (플랫폼별 계정 아이디 관리) |
| ⑤ | social_post_crawl | 수집된 게시물 원본 데이터 |
| ⑥ | social_crawl_account | 크롤링용 로그인 계정 관리 |
| ⑦ | social_crawl_exclude_keyword | 정크/수집 필터 키워드 관리 |

---

### ① social_platform

```sql
platform_id   VARCHAR(50)   PK   -- 'instagram' | 'youtube' | 'x' | 'tiktok'
platform_name VARCHAR(100)
created_at    DATETIME
```

---

### ② brand

```sql
brand_id    BIGINT   PK AUTO_INCREMENT
brand_name  VARCHAR(100)   -- 브랜드 표시명
created_at  DATETIME
updated_at  DATETIME
```

---

### ③ brand_social_channel

브랜드가 운영하는 플랫폼별 채널 정보 (지역 구분 포함)

```sql
channel_id   BIGINT        PK AUTO_INCREMENT
brand_id     BIGINT        FK → brand(brand_id)
platform_id  VARCHAR(50)   FK → social_platform(platform_id)
region       VARCHAR(10)   -- 'KR', 'HQ' 등 지역 구분
channel_url  VARCHAR(200)  -- SNS 채널 전체 URL (미등록 시 NULL)
created_at   DATETIME
updated_at   DATETIME

UNIQUE KEY uq_brand_platform_region (brand_id, platform_id, region)
```

---

### ④ brand_assignee

브랜드 담당자 및 플랫폼별 소셜 계정 ID 관리

```sql
assignee_id   BIGINT        PK AUTO_INCREMENT
brand_id      BIGINT        FK → brand(brand_id)
platform_id   VARCHAR(50)   FK → social_platform(platform_id)
assignee_name VARCHAR(50)   -- 담당자명
account_id    VARCHAR(100)  -- 소셜 미디어 계정 아이디 (@handle 등)
is_active     TINYINT(1)    -- 1: 활성, 0: 비활성
created_at    DATETIME
updated_at    DATETIME
```

---

### ⑤ social_post_crawl

수집된 게시물 원본 데이터 (메인 적재 테이블)

```sql
spc_id           BIGINT UNSIGNED   PK AUTO_INCREMENT

-- 수집 메타
platform_id      VARCHAR(50)       FK → social_platform
crawl_case       VARCHAR(10)       -- 'CASE1': 공식계정 수집 | 'CASE2': 키워드 검색 수집
brand_name       VARCHAR(100)
account_id       VARCHAR(200)      -- 계정 ID / 핸들
account_type     VARCHAR(10)       -- 채널 지역 구분 (brand_social_channel.region 참조)

-- 게시물 정보
post_id          VARCHAR(200)      -- 플랫폼 내 고유 ID (Instagram: shortcode)
post_url         VARCHAR(500)      -- 게시물 원본 URL
post_type        VARCHAR(30)       -- '릴스', '피드', '쇼츠', '영상', '트윗' 등
posted_at        DATETIME          -- 게시 일시
post_title       VARCHAR(255)
text_content     TEXT              -- 캡션/본문 텍스트
person_tags      TEXT              -- 인물 태그 목록 (JSON array)
hashtags         TEXT              -- 해시태그 목록 (JSON array)
media_url        VARCHAR(500)      -- 첫 번째 미디어(이미지/영상) URL
thumbnail_url    TEXT              -- 썸네일 이미지 URL (image_versions2 최소 크기)

-- 통계
view_count       BIGINT
like_count       BIGINT
comment_count    BIGINT
share_count      BIGINT

-- CASE2 전용
matched_keywords TEXT              -- 매칭된 키워드 목록 (JSON array)
author_name      VARCHAR(200)      -- 작성자명 (인플루언서명)
author_followers BIGINT            -- 작성자 팔로워 수

-- 플래그 & 원본
is_duplicate     TINYINT(1)        -- 0: 정상, 1: 중복
is_junk          TINYINT(1)        -- 0: 정상, 1: 정크
raw_data         JSON              -- API 원본 응답 전체 (재처리 대비)

created_at       DATETIME
updated_at       DATETIME

UNIQUE KEY uq_platform_post  (platform_id, post_id)
INDEX idx_brand_platform     (brand_name, platform_id)
INDEX idx_crawl_case         (crawl_case)
INDEX idx_posted_at          (posted_at)
INDEX idx_is_duplicate       (is_duplicate)
INDEX idx_is_junk            (is_junk)
```

---

### ⑥ social_crawl_account

크롤링에 사용하는 로그인 계정 관리 (계정 차단/만료 이슈 관리 포함)

```sql
account_id   BIGINT UNSIGNED   PK AUTO_INCREMENT
name         VARCHAR(100)      -- 계정 별칭 또는 담당자명
platform_id  VARCHAR(50)       FK → social_platform
login_id     VARCHAR(200)      -- 로그인 ID (AES-256-GCM 암호화, Base64 저장)
login_pw     VARCHAR(500)      -- 로그인 PW (AES-256-GCM 암호화, Base64 저장)
issue        TEXT              -- 이슈 사항 (차단, 세션 만료, 2FA 등)
status       VARCHAR(20)       -- 'ACTIVE' | 'BLOCKED' | 'EXPIRED' | 'PAUSED'
created_at   DATETIME
updated_at   DATETIME

UNIQUE KEY uq_platform_login_id (platform_id, login_id)
```

> **암호화 상세** → [9. 자격증명 암호화](#9-자격증명-암호화-social_crawl_account) 참조

---

### ⑦ social_crawl_exclude_keyword

정크 필터 키워드 및 CASE2 수집 필터 키워드 관리

```sql
keyword_id      BIGINT UNSIGNED   PK AUTO_INCREMENT
keyword_type    VARCHAR(20)       -- 'JUNK': 정크 필터 | 'CASE2_FILTER': 수집 포함 필터
platform_id     VARCHAR(50)       FK → social_platform
brand_id        BIGINT UNSIGNED   -- NULL: 전체 공통, 값 있으면 특정 브랜드 전용
filter_keyword  VARCHAR(500)      -- CASE2 수집 필터 키워드
junk_keyword    VARCHAR(500)      -- 정크 필터 키워드
match_type      VARCHAR(20)       -- 'CONTAINS' | 'EXACT' | 'REGEX'
description     VARCHAR(300)      -- 등록 사유
is_active       TINYINT(1)
created_by      VARCHAR(100)
created_at      DATETIME
updated_at      DATETIME
```

---

## 6. Instagram 크롤링 방식

### 6-1. 수집 방법 선택 이유

Instagram은 공식 Graph API가 비즈니스 계정 전용이고 외부 서비스에 대한 접근 제한이 강합니다.  
이에 **Playwright(헤드리스 브라우저 자동화)**를 사용하여 실제 사용자가 브라우저로 접속하는 것과 동일한 방식으로 데이터를 수집합니다.

Instagram 앱/웹은 내부적으로 GraphQL API를 통해 피드 데이터를 가져오는데, 브라우저 세션 상태에서 이 네트워크 요청을 가로채(intercept) 구조화된 JSON 데이터를 추출합니다.

---

### 6-2. 전체 수집 흐름

```
[시작]
  │
  ▼
브라우저 초기화 (Playwright Chromium)
  │  - iPhone 14 Pro Max 모바일 뷰포트 (430×932)
  │  - 봇 감지 우회 스크립트 주입 (webdriver 플래그 제거 등)
  │
  ▼
세션 복원 (instagram_storage.json 존재 시)
  │  - 쿠키 및 localStorage 자동 로드 → 재로그인 불필요
  │
  ▼
로그인 상태 확인
  │  - 로그인 버튼 노출 여부로 판단
  │  - 미로그인 시 → ID/PW 입력 후 로그인 → 세션 파일 저장
  │
  ▼
프로필 페이지 접속 (https://www.instagram.com/{handle}/)
  │  - goto 전에 네트워크 response 리스너 등록 (첫 로드부터 캡처)
  │
  ▼
GraphQL 응답 인터셉트 + 스크롤
  │  - URL에 'graphql/query' 포함된 응답만 파싱
  │  - 엔드포인트: xdt_api__v1__feed__user_timeline_graphql_connection
  │  - 스크롤: 뷰포트의 60~100% 범위를 4~8 단계로 분할 (사람 패턴 모사)
  │  - 최대 50개 게시물 또는 10회 스크롤 시도까지 수집
  │
  ▼
날짜 필터링 (start_dt ~ end_dt, 기본: 전날 00:00 ~ 23:59)
  │
  ▼
키워드 필터링 (CASE2: search_keywords 매칭 확인)
  │
  ▼
SocialPost 객체 변환 → DB 저장
```

---

### 6-3. GraphQL 응답에서 추출하는 필드

Instagram 내부 GraphQL 응답(`xdt_api__v1__feed__user_timeline_graphql_connection`)의 각 `edge.node`에서 아래 필드를 추출합니다.

| GraphQL 필드 | DB 컬럼 | 설명 |
|---|---|---|
| `node.code` | `post_id` | 게시물 고유 shortcode (URL의 `/p/{code}/` 부분) |
| `node.code` 조합 | `post_url` | `https://www.instagram.com/p/{code}/` |
| `node.caption.text` | `text_content` | 캡션 전문 (해시태그/멘션 포함) |
| `node.taken_at` | `posted_at` | Unix timestamp → KST datetime 변환 |
| `node.video_versions[0].url` | `media_url` | 영상 URL (비디오 우선) |
| `node.image_versions2.candidates[0].url` | `media_url` | 이미지 URL (비디오 없을 때) |
| `node.image_versions2.candidates[-1].url` | `thumbnail_url` | 썸네일 URL (candidates 마지막 = 최소 크기) |
| `node.like_count` | `like_count` | 좋아요 수 |
| `node.comment_count` | `comment_count` | 댓글 수 |
| `node.view_count` 또는 `node.play_count` | `view_count` | 조회수 (릴스의 경우 play_count) |
| `data.user.follower_count` | `author_followers` | 계정 팔로워 수 (CASE1 공식 계정) |
| 캡션 regex `@\w+` | `person_tags` | 멘션된 계정 목록 |
| 캡션 regex `#\w+` | `hashtags` | 해시태그 목록 |
| `node` 전체 | `raw_data` | 원본 JSON 전체 (재처리 대비 보존) |

---

### 6-4. 수집 유형 (CASE 구분)

| 구분 | 설명 | 진행 상태 |
|------|------|-----------|
| CASE1 | 브랜드 공식 계정(`@handle`) 프로필 피드 수집 | 구현 완료 |
| CASE2 | 해시태그(`#keyword`) 탐색 페이지 수집 | 코드 작성됨, 현재 비활성 |

---

### 6-5. 봇 감지 우회 전략

| 전략 | 내용 |
|------|------|
| 모바일 뷰포트 | iPhone 14 Pro Max (430×932, scale 3, is_mobile=true) |
| webdriver 플래그 제거 | `navigator.webdriver = undefined` 오버라이드 |
| User-Agent 로테이션 | 실행마다 랜덤 모바일 UA 사용 |
| 랜덤 딜레이 | 페이지 이동 후 10~15초, 스크롤 간 1.5~3초 |
| 스크롤 패턴 모사 | 뷰포트의 60~100%를 4~8 단계로 분할 + ±10px 지터 |
| 쿠키 세션 유지 | `instagram_storage.json`으로 세션 저장/복원 (재로그인 최소화) |
| 알림 권한 우회 | `navigator.permissions.query` 오버라이드 (headless 노출 방지) |

---

### 6-6. 중복 방지 전략

| 레벨 | 방법 |
|------|------|
| DB | `UNIQUE KEY uq_platform_post (platform_id, post_id)` |
| Repository | 저장 전 `exists()` 확인 → `INSERT ... ON DUPLICATE KEY UPDATE` |
| 크롤러 세션 내 | `seen_ids` set으로 동일 세션 내 동일 게시물 중복 스킵 |

---

## 7. 자격증명 암호화 (social_crawl_account)

### 7-1. 알고리즘

| 항목 | 값 |
|------|----|
| 알고리즘 | AES-256-GCM (Galois/Counter Mode) |
| 키 길이 | 256 bit (32 bytes) |
| IV 길이 | 96 bit (12 bytes), 암호화마다 `SecureRandom` 으로 생성 |
| 인증 태그 | 128 bit (GCM 기본값) |
| 키 도출 | 환경변수 `ENCRYPTION_SECRET_KEY` 문자열 → SHA-256 해싱 → 256-bit 키 |
| 저장 형식 | `Base64( IV[12B] \|\| CipherText+AuthTag )` |
| 라이브러리 | Java 표준 `javax.crypto` (외부 의존성 없음) |

### 7-2. 구현 위치

```
backend/src/main/java/com/musinsa/crawler/
└── common/
    └── AesEncryptionUtil.java      # @Component, encrypt() / decrypt()
```

### 7-3. API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| GET | `/api/crawl-accounts` | 전체 목록 (loginId 복호화, loginPw **미포함**) |
| GET | `/api/crawl-accounts/{id}` | 단건 조회 (loginId 복호화, loginPw **미포함**) |
| GET | `/api/crawl-accounts/{id}/decrypt` | loginId + loginPw **원문** 복호화 반환 |
| POST | `/api/crawl-accounts` | 생성 (loginId, loginPw 암호화하여 저장) |
| PUT | `/api/crawl-accounts/{id}` | 수정 (loginId, loginPw 재암호화) |
| DELETE | `/api/crawl-accounts/{id}` | 삭제 |

### 7-4. 운영 키 관리

```bash
# .env 또는 환경변수로 주입 (32자 이상 무작위 문자열 권장)
ENCRYPTION_SECRET_KEY=<운영용_무작위_비밀키>
```

- 개발 기본값: `ChangeThisSecretKeyInProduction!!` (`.env.example` 참조)
- **운영 배포 전 반드시 교체 필요**
- 키가 변경되면 기존 암호화 데이터 복호화 불가 → 키 변경 시 데이터 재암호화 필요

---

## 8. Backend API 엔드포인트 (현재 구현)

| Method | Path | 파라미터 | 설명 |
|--------|------|---------|------|
| GET | `/api/posts` | `platformId`, `brandName`, `crawlCase`, `postedFrom`, `postedTo`, `page`, `size`(기본 20), `sort` | 게시물 목록 (페이징 + 다중 필터) |
| GET | `/api/posts/{spcId}` | - | 게시물 단건 조회 |
| GET | `/api/assignees` | - | 담당자 목록 조회 |
| GET | `/api/crawl-accounts` | - | 크롤 계정 목록 (loginPw 미포함) |
| GET | `/api/crawl-accounts/{id}` | - | 크롤 계정 단건 조회 (loginPw 미포함) |
| GET | `/api/crawl-accounts/{id}/decrypt` | - | loginId + loginPw 원문 복호화 반환 |
| POST | `/api/crawl-accounts` | `SocialCrawlAccountRequest` | 크롤 계정 생성 (201) |
| PUT | `/api/crawl-accounts/{id}` | `SocialCrawlAccountRequest` | 크롤 계정 수정 |
| DELETE | `/api/crawl-accounts/{id}` | - | 크롤 계정 삭제 (204) |

- Spring Data JPA + **QueryDSL** 기반 동적 쿼리 (`SocialPostCrawlRepositoryCustom` / `SocialPostCrawlRepositoryImpl`)
- Service 레이어 없이 Controller → Repository 직접 호출 구조

---

## 9. 현재 개발 상태 및 향후 과제

| 항목 | 상태 |
|------|------|
| Instagram CASE1 (공식 계정 수집) | 구현 완료 |
| Instagram CASE2 (해시태그 검색) | 코드 작성됨, 비활성 |
| DB 저장 연동 | 구현 완료 (`CrawlService`에서 `post_repo.save()` 호출) |
| 정크 키워드 필터링 | 코드 작성됨, 미연결 |
| Slack 알림 | 코드 작성됨, 미연결 |
| TikTok / X 크롤러 | 미구현 |
| AI 요약 (Claude) | 미구현 |
| Frontend 실제 API 연동 | 구현 완료 (DashboardPage: `/api/assignees`, CrawlingStatusPage: `/api/posts`) |
| 크롤 계정 관리 (CRUD) | 구현 완료 (Backend API + Frontend CrawlAccountPage) |
