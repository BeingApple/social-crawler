# Project Overview (2026-03-30)

## 구조
모노레포 멀티모듈: crawler(Python) / backend(Spring Boot) / frontend(React) / db(MySQL DDL)

## Crawler 레이어
- social/ : BaseCrawler ABC + InstagramCrawler (Playwright async)
- service/ : CrawlService(오케스트레이터), SummaryService, MonitoringService
- resource/ : BrandRepository, SocialPostRepository, CrawlJobRepository (PyMySQL raw cursor)
- common/ : types(BrandTarget, SocialPost), utils, http, exceptions
- notifier/ : SlackNotifier (웹훅)
- config/ : DatabaseConfig (PyMySQL 싱글턴)

## Backend 레이어
- api/controller/PostController -> domain/repository/PostRepository -> domain/entity/Post
- Service 레이어 없음 (읽기 전용)

## Frontend 구조
- pages: DashboardPage(계정리스트, 샘플), CrawlingStatusPage(크롤링현황, 샘플), PostListPage(게시물, API연동)
- components/dashboard/DataTable, api/posts, types/{post,brand,crawling}, data/{sampleData,crawlingSampleData}

## 개발 상태
- Instagram 크롤러: 초기 구현 완료 (테스트 모드)
- TikTok/Twitter: 미구현
- CrawlService: 대부분 주석 (저장/필터/알림 미연결)
- Frontend: DashboardPage, CrawlingStatusPage는 샘플데이터 기반