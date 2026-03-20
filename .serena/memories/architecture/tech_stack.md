# brand-social-crawler - 예상 기술 스택

**분석 일시**: 2026-03-20
**유형**: 추론 (빈 레포지토리)

## 권장 기술 스택

### 언어: Python 3.11+
- 크롤링 생태계 (Scrapy, Playwright, BeautifulSoup) 최강
- 데이터 처리 (pandas, pydantic) 풍부
- 무신사 백엔드 스택과 독립적으로 운영 가능

### 크롤링 프레임워크
- **Playwright** (우선) — 헤드리스 브라우저, JS 렌더링 필수인 SNS 대응
- **Scrapy** — 대용량 정적 페이지, 파이프라인 내장
- **httpx + asyncio** — API 기반 수집 (공식 API 활용 시)

### 공식 API 활용
- Instagram Graph API (Meta Business API)
- YouTube Data API v3
- TikTok Research API (제한적)

### 스케줄러
- **Apache Airflow** — 워크플로우 DAG, 무신사 규모에 적합
- **Celery + Redis** — 분산 태스크 큐, 간단한 스케줄링
- **APScheduler** — 경량 스케줄러 (소규모 시작 시)

### 스토리지
- **PostgreSQL** — 정형 데이터 (브랜드 메타, 지표 시계열)
- **MongoDB** — 비정형 원본 데이터 (게시물 전문, 댓글)
- **Redis** — 캐싱, 중복 URL 필터, rate limit 상태
- **S3 / MinIO** — 이미지/영상 원본 보관

### 메시지 큐
- **Kafka** — 대용량 이벤트 스트리밍 (무신사 규모)
- **RabbitMQ** — 경량 메시지 큐 (소규모 시작 시)

### 인프라
- Docker + Kubernetes (무신사 표준 인프라 추정)
- Prometheus + Grafana — 크롤링 성능 모니터링

### 코드 품질
- **Ruff** — 린터/포매터 (Black + flake8 대체)
- **mypy** — 타입 체크
- **pytest** — 테스트
- **pre-commit** — 커밋 전 자동 검사
