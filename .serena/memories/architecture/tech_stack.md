# Tech Stack (2026-03-30)

## Crawler
- Python 3.11, Playwright 1.44, httpx 0.27, PyMySQL 1.1, schedule 1.2
- beautifulsoup4 4.12, instaloader 4.13, python-dotenv 1.0
- SQLAlchemy 2.0 존재하나 전체 주석처리됨 (미사용)

## Backend
- Java 21, Spring Boot 3.3.0, Spring Data JPA, HikariCP
- Lombok, spring-boot-starter-validation
- Gradle 빌드, MySQL Connector/J

## Frontend
- React 18.3, TypeScript 5.5, Vite 8.0
- MUI v5 core + MUI v7 icons/system (버전 혼용 주의)
- MUI X DataGrid v7, React Router v6, axios 1.7

## DB
- MySQL 8.0 (Aurora MySQL 8.0 호환), InnoDB, utf8mb4_unicode_ci

## 인프라
- Docker Compose (4서비스), nginx (SPA + API 프록시), Makefile