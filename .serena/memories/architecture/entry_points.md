# Entry Points (2026-03-30)

## Crawler
- crawler/src/main.py -> main() -> run_all_test() (테스트 모드)
- 운영: run_all() -> DB에서 brand 조회 -> CrawlService.run()
- 실행: python -m src.main 또는 make crawler

## Backend
- backend/src/main/java/com/crawler/CrawlerApplication.java
- 실행: ./gradlew bootRun --args='--spring.profiles.active=local' 또는 make backend

## Frontend
- frontend/src/main.tsx -> App.tsx (LNB + Routes)
- 실행: npm run dev (port 3000) 또는 make frontend

## Docker
- docker-compose up --build 또는 make up
- DB healthcheck 후 crawler/backend 시작, backend 후 frontend 시작