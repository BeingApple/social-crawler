---
description: "단일 명령을 분석하여 crawler/backend/frontend 에이전트에 병렬 분배하고 통합 리뷰까지 수행하는 멀티 모듈 오케스트레이터"
allowed-tools: ["Agent", "Read", "Glob", "Grep", "Bash", "Edit", "Write"]
---

# 멀티 모듈 오케스트레이터

## 작업 요청
$ARGUMENTS

---

## 사전 필독 (모든 단계 시작 전 반드시 수행)

아래 두 파일을 순서대로 읽는다. 내용을 충분히 숙지한 후 다음 단계로 넘어간다.

1. `CLAUDE.md` — 프로젝트 개요, DB 스키마, API 엔드포인트, 컨벤션, 제약사항
2. `docs/architecture.md` — 시스템 아키텍처, 모듈 간 의존성, 기술적 의사결정 이력

두 파일의 내용이 서로 충돌할 경우, 사용자에게 충돌 내용을 명시하고 어떤 문서를 우선할지 확인한다.
사용자도 판단하기 어렵다고 하거나 응답이 모호한 경우, 실제 코드를 읽어 현재 구현 상태를 기준으로 판단한다.

---

## 프로젝트 컨텍스트

이 프로젝트는 브랜드 소셜 미디어 크롤링 파이프라인으로, 아래 4개 모듈로 구성된 모노레포다.

| 모듈 | 경로 | 언어/스택 |
|------|------|-----------|
| **crawler** | `crawler/` | Python 3.11, Playwright, PyMySQL |
| **backend** | `backend/` | Java 21, Spring Boot 3.3, JPA, QueryDSL |
| **frontend** | `frontend/` | React 18, TypeScript 5.5, MUI v7 |
| **db** | `db/init/` | MySQL 8.0, DDL SQL |

---

## ① 오케스트레이터 분석 (반드시 먼저 수행)

작업 요청을 분석하여 아래 항목을 결정한다.

### 1-1. 영향 모듈 판별

각 모듈의 영향 여부를 판단하는 기준:

- **db**: 테이블 컬럼 추가/변경/삭제, 새 테이블, 인덱스 변경
- **crawler**: 크롤링 로직, 새 플랫폼, 파싱 방법, DB 저장 로직, 스케줄러
- **backend**: API 엔드포인트 추가/변경, Entity/DTO, 비즈니스 로직, 암호화
- **frontend**: UI 화면, 컴포넌트, API 연동, 타입 정의

### 1-2. 의존성 그래프 결정

아래 규칙으로 실행 순서를 결정한다.

```
db 변경 있음    → db 먼저 → (crawler ‖ backend) 병렬 → frontend 마지막
API 계약 변경   → backend 먼저 → frontend
크롤러만 변경   → crawler 독립 실행
UI만 변경       → frontend 독립 실행
backend만 변경  → backend 독립 실행
전체 새 기능    → db → (crawler ‖ backend) → frontend
```

### 1-3. 분석 결과 출력

아래 형식으로 분석 결과를 사용자에게 먼저 보여주고 진행한다:

```
📋 작업 분석 결과
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 작업 요약: [한 줄 요약]

📦 영향 모듈:
  ✅ db       — [변경 이유 또는 해당 없음이면 표시 안 함]
  ✅ crawler  — [변경 이유]
  ✅ backend  — [변경 이유]
  ✅ frontend — [변경 이유]

🔗 실행 순서: db → (crawler ‖ backend) → frontend
   (병렬 가능한 모듈은 ‖ 표시)

⚠️  교차 모듈 계약:
  - [API 스펙 변경 사항]
  - [DB 스키마 계약]
  - [TypeScript 타입 변경]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## ② 모듈별 작업 명세 생성

영향받는 각 모듈에 대해 구체적인 작업 명세를 작성한다.

각 명세에는 반드시 포함:
- 변경할 파일 목록 (경로 포함)
- 변경 내용 상세 (추가/수정/삭제)
- 다른 모듈과의 인터페이스 계약 (API 스펙, 타입, 스키마)
- 변경하지 말아야 할 것 (사이드 이펙트 방지)

---

## ③ 에이전트 실행

### 서브 에이전트 사용 기준

아래 기준으로 판단하여 Agent 툴 사용 여부를 결정한다.

**서브 에이전트를 사용한다:**
- 병렬 가능(`‖`) 모듈 → 단일 응답에서 Agent 툴을 **동시에 여러 개** 호출 (필수)
- 파일 3개 이상 읽기/수정이 필요한 모듈
- 어느 파일을 수정해야 할지 탐색이 필요한 경우

**메인에서 직접 처리한다:**
- 수정 파일이 1~2개이고 위치와 내용이 이미 명확한 경우
- 에이전트 생성 오버헤드가 작업 규모보다 큰 경우

### 에이전트 공통 지침 (각 에이전트 프롬프트에 포함)

```
이 프로젝트의 CLAUDE.md에 정의된 프로젝트 컨텍스트와 DB 스키마를 참고할 것.
코드 변경 시 기존 패턴과 컨벤션을 반드시 따를 것.
요청된 변경 외에 리팩토링, 주석 추가, 불필요한 개선을 하지 말 것.
변경한 파일 목록과 변경 내용을 반드시 반환할 것.
```

### db 에이전트 (선행 실행, 해당 시)

```
역할: db/init/01_schema.sql 파일의 DDL 수정
작업: [② 에서 작성한 db 명세]
반환: 변경된 SQL 스니펫 (변경 전/후)
주의: 기존 테이블 DROP/TRUNCATE 금지. ALTER TABLE 또는 새 테이블만.
```

### crawler 에이전트 (db 완료 후 또는 독립)

```
역할: crawler/ 디렉토리의 Python 크롤러 코드 수정
기술: Python 3.11, Playwright async, PyMySQL raw cursor, asyncio
패턴:
  - BaseCrawler ABC 상속 패턴 (crawl_official_account, crawl_search)
  - Repository 패턴 (BrandRepository, SocialPostRepository)
  - DatabaseConfig 싱글턴 커넥션 (config/database.py)
  - SQLAlchemy 코드(db.py, models.py)는 주석 처리 상태 — 건드리지 말 것
작업: [② 에서 작성한 crawler 명세]
반환: 변경된 파일 목록 + 변경 전/후 코드 스니펫
```

### backend 에이전트 (db 완료 후 또는 독립)

```
역할: backend/ 디렉토리의 Spring Boot API 수정
기술: Java 21, Spring Boot 3.3, JPA, QueryDSL, Lombok
패턴:
  - Controller → Service → Repository 레이어 구조를 반드시 사용할 것
    (기존 코드가 Controller → Repository 직접 호출이더라도 새 코드는 Service 레이어를 추가)
  - QueryDSL 동적 쿼리는 SocialPostCrawlRepositoryImpl 패턴 참고
  - AES-256-GCM 암호화는 AesEncryptionUtil 사용
  - DTO에 from() 팩토리 메서드 패턴 사용
  - 기존 엔드포인트: GET /api/posts, /api/assignees, /api/crawl-accounts (CRUD)
작업: [② 에서 작성한 backend 명세]
반환: 변경된 파일 목록 + 변경 전/후 코드 스니펫 + 새 API 스펙 (있는 경우)
```

### frontend 에이전트 (backend 완료 후 또는 독립)

```
역할: frontend/src/ 디렉토리의 React 컴포넌트 수정
기술: React 18, TypeScript 5.5, MUI v7, MUI X DataGrid v7, axios
패턴:
  - 타입은 frontend/src/types/ 에 정의
  - API 클라이언트는 frontend/src/api/ 에 정의 (axios 기반)
  - 페이지 컴포넌트는 frontend/src/pages/
  - LNB 라우팅은 App.tsx에서 관리 (경로 추가 시 App.tsx도 수정)
  - API URL은 /api/* 경로 사용 (nginx 프록시)
작업: [② 에서 작성한 frontend 명세]
반환: 변경된 파일 목록 + 변경 전/후 코드 스니펫
```

---

## ④ 문서 업데이트 (모든 에이전트 완료 후, 리뷰 전)

변경사항이 아래 항목에 해당하면 **반드시** 해당 문서를 업데이트한다.

### CLAUDE.md 업데이트 대상
- `## Project Analysis` 섹션의 DB 스키마 변경 (테이블/컬럼 추가·수정·삭제)
- API 엔드포인트 추가·변경
- 기술 스택 변경 (새 라이브러리, 언어 버전 등)
- 핵심 컴포넌트 상태 변경 (구현 완료 → 미완, 또는 반대)
- 환경변수 추가·변경

### docs/architecture.md 업데이트 대상
- 모듈 간 의존성 변경 (새 서비스 호출, 제거된 의존성)
- 새로운 아키텍처 패턴 도입
- 기술적 의사결정(ADR) 추가

### 업데이트 방식
- 내용이 변경된 섹션만 수정한다 (전체 재작성 금지)
- 변경 이유가 명확하지 않으면 기존 내용을 유지한다

---

## ⑤ 통합 리뷰 (모든 에이전트 완료 후)

모든 모듈 에이전트 완료 후 통합 리뷰를 수행한다.

### 검증 체크리스트

**계약 일치 검증**
- [ ] Backend API 응답 형식과 Frontend 타입 정의가 일치하는가?
- [ ] DB 스키마 변경이 Crawler Repository와 Backend Entity에 모두 반영되었는가?
- [ ] 새 API 엔드포인트가 nginx.conf 프록시 범위(`/api/*`) 내에 있는가?

**사이드 이펙트 검증**
- [ ] 기존 API 엔드포인트가 깨지지 않았는가? (Breaking change 없음)
- [ ] Crawler의 `uq_platform_post (platform_id, post_id)` 중복 방지 로직이 유지되는가?
- [ ] `social_crawl_account` 암호화/복호화 흐름이 변경되지 않았는가?
- [ ] Frontend 라우팅(`/accounts`, `/crawling`, `/crawl-accounts`)이 정상 동작하는가?

**코드 품질**
- [ ] TypeScript 타입 에러 없음 (`any` 타입 신규 사용 없음)
- [ ] Java `@NotNull`/`@Valid` 등 Validation 어노테이션 누락 없음
- [ ] Python 비동기 코드에서 `await` 누락 없음

### 리뷰 결과 출력 형식

```
🔍 통합 리뷰 결과
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
판정: ✅ Approve / ⚠️ Request Changes / ❌ Reject

📦 변경 요약:
  - db: [변경 내용]
  - crawler: [변경 내용]
  - backend: [변경 내용]
  - frontend: [변경 내용]

📄 문서 업데이트:
  - CLAUDE.md: [업데이트된 섹션 또는 변경 없음]
  - docs/architecture.md: [업데이트된 섹션 또는 변경 없음]

🔗 계약 검증: [이상 없음 / 이슈 목록]
⚠️  사이드 이펙트: [없음 / 발견된 이슈]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Request Changes 판정 시: 해당 모듈 에이전트 재실행 (최대 2회).
Reject 판정 시: 즉시 사용자에게 보고하고 중단.

---

## 실행 흐름 요약

```
① 분석 → 사용자에게 결과 보고 (계속 진행 확인)
② 명세 작성
③ 에이전트 실행 (의존성 순서 준수)
④ 문서 업데이트 (CLAUDE.md, docs/architecture.md)
⑤ 통합 리뷰
⑥ 최종 결과 보고
```

> **중요**: 사용자 확인 없이 파일을 삭제하거나 기존 API를 제거하지 않는다.
> DB DDL 변경은 항상 후진 호환성(backward compatibility)을 유지한다 (컬럼 삭제 금지, NOT NULL 추가 시 DEFAULT 필수).
