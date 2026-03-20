# brand-social-crawler - 데이터 아키텍처 패턴

**분석 일시**: 2026-03-20

## 데이터 흐름 (추론)

```
[SNS 플랫폼] → [Crawler] → [Message Queue] → [Parser] → [Storage]
                                                              ↓
                                                    [API Server] → [내부 소비자]
```

## 스토리지 레이어 분리

### Writer 레이어
- 크롤러 → Kafka/RabbitMQ → Consumer → DB Insert
- 원본 raw 데이터는 MongoDB 또는 S3에 별도 보관
- 정제된 지표 데이터는 PostgreSQL 시계열 테이블

### Reader 레이어
- PostgreSQL Read Replica → API 응답
- Redis 캐시 → 자주 조회되는 브랜드 지표

## 핵심 데이터 모델 (예상)

### brands 테이블
- brand_id, brand_name, musinsa_brand_code
- instagram_handle, youtube_channel_id, tiktok_username
- created_at, updated_at, is_active

### social_metrics 테이블 (시계열)
- brand_id, platform, metric_type, metric_value
- collected_at, period (daily/hourly)

### posts 테이블
- post_id, brand_id, platform, external_post_id
- content, media_urls, hashtags
- likes, comments, shares, views
- posted_at, crawled_at

## 중복 수집 방지
- Redis SET에 post_id 저장 (TTL 30일)
- DB unique constraint on (platform, external_post_id)
