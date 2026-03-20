# brand-social-crawler - 예상 진입점 및 컴포넌트

**분석 일시**: 2026-03-20

## 예상 주요 진입점

### 스케줄러 진입점
- `src/scheduler/main.py` — 크론 스케줄러 메인 루프
- `src/scheduler/dag/` — Airflow DAG 정의 (사용 시)

### 크롤러 진입점
- `src/crawlers/instagram_crawler.py`
- `src/crawlers/youtube_crawler.py`
- `src/crawlers/tiktok_crawler.py`

### API 서버 진입점
- `src/api/main.py` — FastAPI/Flask 앱 초기화

### CLI 진입점
- `src/cli.py` — 수동 크롤링 트리거, 재수집 명령

## 예상 컴포넌트 상세

### Crawler 컴포넌트
- BaseCrawler (추상 클래스) → 플랫폼별 구현체
- Rate Limiter (토큰 버킷 알고리즘)
- Proxy Rotator (IP 차단 우회)
- Session Manager (쿠키/토큰 관리)

### Parser 컴포넌트
- HTMLParser — Playwright 렌더링 결과 파싱
- APIResponseParser — 공식 API JSON 파싱
- DataNormalizer — 플랫폼별 데이터 통일 스키마 변환

### Storage 컴포넌트
- PostgreSQLWriter / PostgreSQLReader
- MongoDBWriter (원본 데이터)
- RedisCache

### Monitoring 컴포넌트
- CrawlMetricsCollector (성공률, 수집량, 레이턴시)
- AlertManager (임계값 초과 시 Slack/PagerDuty 알림)
