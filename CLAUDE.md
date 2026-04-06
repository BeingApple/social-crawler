# brand-social-crawler — Claude 컨텍스트

## 프로젝트 개요

브랜드의 소셜 미디어 데이터를 **매일 전날 기준**으로 수집하고, AI 요약 후 Slack으로 알림을 제공하는 크롤링 파이프라인.

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

- 서버: dev EC2
- DB: dev DB
- Slack Hook / Claude Hook: 내부 제공

## 기술 스택 (구현 완료)

| 모듈 | 스택 |
|------|------|
| **Crawler** | Python 3.11, Playwright, BeautifulSoup4, SQLAlchemy 2.0, schedule |
| **Backend** | Java 21, Spring Boot 3.3, Spring Data JPA, Lombok |
| **Frontend** | React 18, **TypeScript 5.5**, Vite 8, MUI v7, MUI X DataGrid v7, React Router v6, axios |
| **DB** | MySQL 8.0 (Aurora MySQL 8.0 호환) |
| **인프라** | Docker Compose, nginx (프론트 서빙 + API 프록시) |

## 핵심 데이터 모델 (설계 기준)

```sql
-- 브랜드
brand_id, brand_name, brand_code,
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

> 상세 분석 내용은 [`docs/project-analysis.md`](docs/project-analysis.md) 참조.

