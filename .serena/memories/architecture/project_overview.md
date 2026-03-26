# brand-social-crawler - Project Overview

**분석 일시**: 2026-03-26
**분석 유형**: 실제 구현 기반 (4모듈 완성)
**회사**: Musinsa (무신사)

## 프로젝트 목적

무신사 입점 브랜드의 소셜 미디어 데이터(Instagram, TikTok, Twitter)를 자동 수집·저장하고,
어드민 대시보드에서 조회할 수 있는 풀스택 크롤링 파이프라인.

## 4개 Docker 서비스 구성

| 서비스 | 컨테이너명 | 포트 | 기술 |
|--------|-----------|------|------|
| db | crawler-db | 3306 | MySQL 8.0 |
| crawler | crawler-python | — | Python 3.11 + Playwright |
| backend | crawler-backend | 8080 | Java 21 + Spring Boot 3.3 |
| frontend | crawler-frontend | 3000 | React 18 + Vite + MUI v5 |

## 실제 디렉토리 구조

```
brand-social-crawler/
├── docker-compose.yml
├── .env.example
├── db/init/01_schema.sql
├── crawler/src/
│   ├── db.py          # SQLAlchemy 세션
│   ├── models.py      # Brand, Post ORM
│   ├── crawler.py     # Playwright + BS4
│   └── main.py        # schedule 엔트리포인트
├── backend/src/main/java/com/musinsa/crawler/
│   ├── domain/entity/Post.java
│   ├── domain/repository/PostRepository.java
│   ├── api/controller/PostController.java
│   └── api/dto/PostResponse.java
└── frontend/src/
    ├── main.jsx / App.jsx
    ├── api/posts.js
    └── pages/PostListPage.jsx
```

## 상태

- 4모듈 구현 완료 (docker-compose 기반 로컬 실행 가능)
- 실제 크롤링 로직은 `crawler.py`에 더미 Insert로 대체 (주석으로 실제 코드 안내)
- 확장 포인트: 플랫폼별 크롤러 분리, Brand API 추가, social_metrics 테이블 추가
