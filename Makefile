# ─── brand-social-crawler 편의 명령어 ─────────────────────────────────────────
# 사용법: make <target>

.PHONY: help up down db backend frontend crawler setup-python

help:            ## 명령어 목록 출력
	@grep -E '^[a-zA-Z_-]+:.*##' Makefile | awk 'BEGIN {FS=":.*## "}; {printf "  %-18s %s\n", $$1, $$2}'

# ── Docker ────────────────────────────────────────────────────────────────────
up:              ## 전체 스택 빌드 & 실행 (docker-compose)
	docker-compose up --build

down:            ## 전체 스택 종료
	docker-compose down

up-bg:           ## 전체 스택 백그라운드 실행
	docker-compose up --build -d

db:              ## DB만 실행 (로컬 개발 시 Backend/Crawler 직접 실행과 병행)
	docker-compose up db

# ── Backend (로컬 직접 실행) ───────────────────────────────────────────────────
backend:         ## Spring Boot 로컬 실행 (DB는 별도 기동 필요)
	cd backend && ./gradlew bootRun --args='--spring.profiles.active=local'

backend-build:   ## Spring Boot JAR 빌드
	cd backend && ./gradlew bootJar

# ── Frontend (로컬 직접 실행) ──────────────────────────────────────────────────
frontend:        ## React 개발 서버 실행 (http://localhost:3000)
	cd frontend && npm install && npm run dev

# ── Crawler (로컬 직접 실행) ───────────────────────────────────────────────────
setup-python:    ## Python 가상환경 + 의존성 설치 (최초 1회)
	cd crawler && bash setup_venv.sh

crawler:         ## Crawler 로컬 실행 (venv + DB 기동 필요)
	cd crawler && .venv/bin/python -m src.main

# ── 유틸 ──────────────────────────────────────────────────────────────────────
logs:            ## 전체 서비스 로그 출력
	docker-compose logs -f

ps:              ## 실행 중인 컨테이너 목록
	docker-compose ps
