FROM python:3.11-slim-bookworm

# Playwright 시스템 의존성
RUN apt-get update && apt-get install -y --no-install-recommends \
        wget curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright 브라우저 설치 (Chromium만)
RUN playwright install chromium --with-deps

COPY src/ ./src/

CMD ["python", "-m", "src.main"]
