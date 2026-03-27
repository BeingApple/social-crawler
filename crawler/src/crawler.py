"""
크롤러 예시 — Playwright(JS 렌더링) + BeautifulSoup(파싱).

실제 운영 시에는 플랫폼별로 별도 모듈로 분리하세요.
여기서는 더미 데이터를 사용해 DB Insert 흐름만 확인합니다.
"""

'''
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Generator

from playwright.sync_api import sync_playwright, Page
from bs4 import BeautifulSoup

from src.db import SessionLocal
from src.models import Brand, Post

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────
# 공개 타임라인 크롤 (예시: 더미 페이지 파싱)
# ──────────────────────────────────────────────────

def _fetch_html(url: str) -> str:
    """Playwright로 JS 렌더링 후 HTML 반환."""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page: Page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=30_000)
        html = page.content()
        browser.close()
    return html


def _parse_posts(html: str, brand_id: int, platform: str) -> list[dict]:
    """
    BeautifulSoup으로 게시물 목록 파싱.
    실제 셀렉터는 대상 사이트에 맞게 수정하세요.
    """
    soup = BeautifulSoup(html, "html.parser")
    results: list[dict] = []

    # TODO: 실제 사이트 셀렉터로 교체
    for item in soup.select(".post-item"):
        results.append({
            "brand_id": brand_id,
            "platform": platform,
            "external_post_id": item.get("data-id", "unknown"),
            "content": item.select_one(".post-content").get_text(strip=True) if item.select_one(".post-content") else None,
            "likes": int(item.get("data-likes", 0)),
            "comments": int(item.get("data-comments", 0)),
            "posted_at": datetime.now(tz=timezone.utc),
        })

    return results


def _upsert_posts(rows: list[dict]) -> None:
    """중복 외부 ID는 무시하고 신규 게시물만 INSERT."""
    with SessionLocal() as session:
        for row in rows:
            exists = (
                session.query(Post)
                .filter_by(platform=row["platform"], external_post_id=row["external_post_id"])
                .first()
            )
            if not exists:
                session.add(Post(**row))
        session.commit()
        logger.info("Upserted %d posts.", len(rows))


# ──────────────────────────────────────────────────
# 더미 데이터 INSERT (실제 크롤링 대신 테스트용)
# ──────────────────────────────────────────────────

def insert_dummy_posts() -> None:
    """개발/테스트용 더미 게시물 DB 적재."""
    with SessionLocal() as session:
        brand = session.query(Brand).filter_by(platform="instagram", is_active=1).first()
        if not brand:
            logger.warning("활성 브랜드 없음 — 더미 Insert 건너뜀")
            return

        dummy = Post(
            brand_id=brand.brand_id,
            platform="instagram",
            external_post_id=f"dummy_{int(datetime.utcnow().timestamp())}",
            content="테스트 게시물입니다 #musinsa #fashion",
            hashtags=["musinsa", "fashion"],
            likes=120,
            comments=5,
            views=3000,
            posted_at=datetime.utcnow(),
        )
        session.add(dummy)
        session.commit()
        logger.info("더미 게시물 Insert 완료 (post_id=%d)", dummy.post_id)


# ──────────────────────────────────────────────────
# 브랜드별 크롤 실행
# ──────────────────────────────────────────────────

def run_all() -> None:
    logger.info("=== 크롤링 시작 ===")

    # 개발 단계에서는 더미 Insert로 흐름 확인
    insert_dummy_posts()

    # 실제 크롤링 활성화 시 아래 블록을 언주석
    # with SessionLocal() as session:
    #     brands = session.query(Brand).filter_by(is_active=1).all()
    # for brand in brands:
    #     url = f"https://example.com/{brand.account_handle}"
    #     html = _fetch_html(url)
    #     rows = _parse_posts(html, brand.brand_id, brand.platform)
    #     _upsert_posts(rows)

    logger.info("=== 크롤링 완료 ===")
'''