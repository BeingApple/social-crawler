# brand-social-crawler - Project Overview

**분석 일시**: 2026-03-20
**분석 유형**: 추론 분석 (빈 레포지토리 — 코드 없음)
**회사**: Musinsa (무신사) — 한국 최대 패션 이커머스 플랫폼
**GitHub**: https://github.com/musinsa/brand-social-crawler

## 프로젝트 목적 (추론)
브랜드 소셜 크롤러는 무신사 입점 브랜드들의 소셜 미디어 활동 데이터를 수집·분석하는 시스템이다.

### 핵심 역할 (Musinsa 컨텍스트)
- 입점 브랜드의 인스타그램/유튜브/틱톡 등 SNS 게시물 수집
- 브랜드별 소셜 지표 (팔로워, 좋아요, 댓글, 조회수) 트래킹
- 패션 트렌드 감지 및 신제품 런칭 조기 포착
- 브랜드 영향력 지수 산출 → 입점 심사 또는 마케팅 의사결정 지원
- 경쟁 브랜드 벤치마킹 데이터 제공

## 예상 디렉토리 구조 (설계 제안)
```
brand-social-crawler/
├── src/
│   ├── crawlers/          # 플랫폼별 크롤러 (instagram, youtube, tiktok)
│   ├── parsers/           # HTML/JSON 파싱 로직
│   ├── storage/           # DB 연동 (write/read 분리)
│   ├── scheduler/         # 크론 스케줄러
│   ├── api/               # 내부 API (결과 조회용)
│   └── utils/             # 공통 유틸 (rate limiter, proxy 등)
├── tests/
├── config/
├── docker/
└── docs/
```

## 크롤링 대상 플랫폼 (우선순위 추론)
1. Instagram — 패션 브랜드 주력 채널, 팔로워/게시물/릴스
2. YouTube — 브랜드 룩북/캠페인 영상, 조회수/구독자
3. TikTok — Z세대 패션 소비 트렌드, 숏폼 콘텐츠
4. Twitter/X — 실시간 브랜드 언급, 해시태그 트래킹

## 상태
- 빈 레포지토리 (초기화 단계)
- 아키텍처 설계 및 기술 스택 선정 필요
