#!/bin/bash
# ─── Python 가상환경 초기 세팅 스크립트 ───────────────────────────────────────
# IntelliJ에서 Crawler를 로컬 실행하기 전에 1회만 실행하면 됩니다.
# 사용법: cd crawler && bash setup_venv.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

echo "=== Python 가상환경 생성 ==="
python3 -m venv "$VENV_DIR"

echo "=== 의존성 설치 ==="
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"

echo "=== Playwright 브라우저 설치 ==="
"$VENV_DIR/bin/playwright" install chromium

echo ""
echo "✅ 완료! IntelliJ Python 인터프리터 경로:"
echo "   $VENV_DIR/bin/python"
echo ""
echo "IntelliJ 설정 방법:"
echo "  File → Project Structure → SDKs → (+) Python SDK"
echo "  → Virtualenv Environment → Existing → 위 경로 선택"
