from __future__ import annotations

import asyncio
import json
import logging
import os
import random
import re
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from src.common.types import SocialPost
from src.common.utils import contains_any, random_user_agent
from src.social.base import BaseCrawler

logger = logging.getLogger(__name__)


@dataclass
class InstagramPageData:
    post_id: str
    url: str
    content: str
    likes: int = 0
    comments: int = 0
    views: int = 0
    posted_at: datetime | None = None


class InstagramCrawler(BaseCrawler):
    """Playwright 기반 Instagram 크롤러"""

    platform = "instagram"
    BASE_URL = "https://www.instagram.com"

    def __init__(
            self,
            proxy: dict[str, str] | None = None,
            user_agent: str | None = None,
            headless: bool = True,
    ) -> None:
        self._proxy = proxy
        self._user_agent = user_agent or random_user_agent()
        self._headless = headless

        # 쿠키 저장 경로
        self._storage_dir = Path(__file__).resolve().parent.parent.parent
        self._storage_file = self._storage_dir / "instagram_storage.json"

        # 인증 정보
        self._username = os.getenv("INSTAGRAM_USERNAME", "")
        self._password = os.getenv("INSTAGRAM_PASSWORD", "")

        # Playwright 객체 (lazy init)
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None

    async def _init_browser(self) -> BrowserContext:
        """브라우저 및 컨텍스트 초기화"""
        if self._context:
            return self._context

        playwright = await async_playwright().start()

        # 브라우저 시작 옵션
        launch_options: dict[str, Any] = {
            "headless": self._headless,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        }

        # 프록시 설정
        if self._proxy:
            launch_options["proxy"] = {
                "server": self._proxy.get("http") or self._proxy.get("https", ""),
            }

        self._browser = await playwright.chromium.launch(**launch_options)

        # 컨텍스트 옵션 (모바일처럼 보이게)
        context_options: dict[str, Any] = {
            "user_agent": self._user_agent,
            "viewport": {"width": 430, "height": 932},  # iPhone 14 Pro Max
            "device_scale_factor": 3,
            "is_mobile": True,
            "has_touch": True,
            "locale": "ko-KR",
            "timezone_id": "Asia/Seoul",
        }

        # 저장된 세션(쿠키) 로드
        if self._storage_file.exists():
            context_options["storage_state"] = str(self._storage_file)
            logger.info("instagram session loaded from %s", self._storage_file)

        self._context = await self._browser.new_context(**context_options)

        # 봇 감지 우회 스크립트
        await self._context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
        """)

        return self._context

    async def _login(self, page: Page) -> bool:
        """Instagram 로그인 수행"""
        if not self._username or not self._password:
            logger.warning("instagram credentials not set")
            return False

        try:
            await page.goto(f"{self.BASE_URL}/accounts/login/", wait_until="networkidle")
            await self._random_delay(10, 20)

            # 쿠키 동의 버튼 (있으면 클릭)
            try:
                cookie_btn = page.locator("button:has-text('허용'), button:has-text('Allow')")
                if await cookie_btn.count() > 0:
                    await cookie_btn.first.click()
                    await self._random_delay(1, 2)
            except Exception:
                pass

            # 로그인 폼 입력
            username_input = page.locator('input[name="email"]')
            password_input = page.locator('input[name="pass"]')

            await username_input.fill(self._username)
            await self._random_delay(0.5, 1)
            await password_input.fill(self._password)
            await self._random_delay(0.5, 1)

            # 로그인 버튼 클릭
            #login_btn = page.locator('button[type="submit"]')
            login_btn = page.locator('div[aria-label="로그인"]')
            await login_btn.click()

            # 로그인 완료 대기
            await page.wait_for_url(f"{self.BASE_URL}/**", timeout=30000)
            await self._random_delay(3, 5)

            # 세션 저장
            if self._context:
                await self._context.storage_state(path=str(self._storage_file))
                logger.info("instagram session saved to %s", self._storage_file)

            return True

        except Exception as e:
            logger.error("instagram login failed: %s", e)
            return False

    async def _check_login_status(self, page: Page) -> bool:
        """로그인 상태 확인"""
        try:
            await page.goto(self.BASE_URL, wait_until="networkidle", timeout=30000)
            await self._random_delay(10, 12)

            # 로그인 버튼이 보이면 미로그인 상태
            #login_link = page.locator('a[href="/accounts/login/"]')
            login_link = page.locator('div[aria-label="로그인"]')
            if await login_link.count() > 0:
                return False

            # 프로필 아이콘이 보이면 로그인 상태
            #profile_icon = page.locator('svg[aria-label="홈"], svg[aria-label="Home"]')
            profile_icon = page.locator('img[crossorigin="anonymous"]')
            return await profile_icon.count() > 0

        except Exception as e:
            print("_check_login_status : " + e.__class__.__name__, e)
            return False

    async def _parse_post_data(self, page: Page, shortcode: str) -> InstagramPageData | None:
        """개별 게시물 페이지에서 데이터 추출"""
        try:
            url = f"{self.BASE_URL}/p/{shortcode}/"
            await page.goto(url, wait_until="networkidle")
            await self._random_delay(2, 4)

            # JSON-LD 또는 meta 태그에서 데이터 추출
            content = ""
            likes = 0
            comments = 0
            views = 0
            posted_at = None

            # 캡션 추출
            try:
                caption_el = page.locator('h1, span:has-text("")').first
                content = await caption_el.inner_text() if await caption_el.count() > 0 else ""
            except Exception:
                pass

            # 좋아요 수 추출 (다양한 셀렉터 시도)
            try:
                likes_text = await page.locator('section span:has-text("좋아요"), section span:has-text("likes")').first.inner_text()
                likes = self._parse_count(likes_text)
            except Exception:
                pass

            # 조회수 추출 (릴스/동영상)
            try:
                views_text = await page.locator('span:has-text("회 재생"), span:has-text("views")').first.inner_text()
                views = self._parse_count(views_text)
            except Exception:
                pass

            # 게시 시간 추출
            try:
                time_el = page.locator("time")
                if await time_el.count() > 0:
                    datetime_str = await time_el.first.get_attribute("datetime")
                    if datetime_str:
                        posted_at = datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
            except Exception:
                pass

            return InstagramPageData(
                post_id=shortcode,
                url=url,
                content=content,
                likes=likes,
                comments=comments,
                views=views,
                posted_at=posted_at,
            )

        except Exception as e:
            logger.warning("failed to parse post %s: %s", shortcode, e)
            return None

    @staticmethod
    def _parse_count(text: str) -> int:
        """'1.2만', '1,234', '1.5K' 형식을 숫자로 변환"""
        text = text.strip().replace(",", "").replace(" ", "")

        multipliers = {"k": 1000, "K": 1000, "만": 10000, "m": 1000000, "M": 1000000}

        for suffix, mult in multipliers.items():
            if suffix in text:
                try:
                    num = float(re.sub(r"[^\d.]", "", text.replace(suffix, "")))
                    return int(num * mult)
                except ValueError:
                    return 0

        try:
            return int(re.sub(r"[^\d]", "", text))
        except ValueError:
            return 0

    @staticmethod
    async def _random_delay(min_sec: float = 1.0, max_sec: float = 3.0) -> None:
        """봇 감지 방지를 위한 랜덤 대기"""
        await asyncio.sleep(random.uniform(min_sec, max_sec))

    async def _scroll_and_collect_posts(
            self,
            page: Page,
            start_dt: datetime,
            end_dt: datetime,
            max_posts: int = 50,
    ) -> list[str]:
        """프로필 페이지 스크롤하며 게시물 shortcode 수집"""
        shortcodes: list[str] = []
        last_height = 0
        scroll_attempts = 0
        max_scroll_attempts = 10

        while len(shortcodes) < max_posts and scroll_attempts < max_scroll_attempts:
            # 게시물 링크 수집
            links = await page.locator('a[href*="/p/"]').all()

            for link in links:
                href = await link.get_attribute("href")
                if href and "/p/" in href:
                    # /p/ABC123/ 에서 ABC123 추출
                    match = re.search(r"/p/([^/]+)/", href)
                    if match:
                        code = match.group(1)
                        if code not in shortcodes:
                            shortcodes.append(code)

            # 스크롤
            current_height = await page.evaluate("document.body.scrollHeight")
            if current_height == last_height:
                scroll_attempts += 1
            else:
                scroll_attempts = 0

            last_height = current_height
            await page.evaluate("window.scrollBy(0, window.innerHeight)")
            await self._random_delay(1.5, 3)

        return shortcodes[:max_posts]

    def crawl_official_account(
            self,
            brand_id: int,
            handle: str,
            search_keywords: list[str],
            start_dt: datetime,
            end_dt: datetime,
    ) -> list[SocialPost]:
        """공식 계정 크롤링 (동기 래퍼)"""
        return asyncio.run(
            self._crawl_official_account_async(
                brand_id, handle, search_keywords, start_dt, end_dt
            )
        )
        '''
        return asyncio.get_event_loop().run_until_complete(
            self._crawl_official_account_async(
                brand_id, handle, search_keywords, start_dt, end_dt
            )
        )
        '''

    async def _crawl_official_account_async(
            self,
            brand_id: int,
            handle: str,
            search_keywords: list[str],
            start_dt: datetime,
            end_dt: datetime,
    ) -> list[SocialPost]:
        """공식 계정 크롤링 (비동기)"""
        start_time = time.perf_counter()
        posts: list[SocialPost] = []

        try:
            context = await self._init_browser()
            page = await context.new_page()

            # 로그인 상태 확인 및 로그인
            if not await self._check_login_status(page):
                if not await self._login(page):
                    logger.error("instagram login failed, cannot crawl")
                    return posts

            # 프로필 페이지로 이동
            profile_url = f"{self.BASE_URL}/{handle}/"
            await page.goto(profile_url, wait_until="networkidle", timeout=30000) # 30초
            await self._random_delay(10, 15)

            # 프로필 존재 확인
            if "페이지를 찾을 수 없습니다" in await page.content():
                logger.warning("instagram profile not found: %s", handle)
                return posts

            logger.info("instagram crawl started for @%s", handle)

            # 게시물 shortcode 수집
            shortcodes = await self._scroll_and_collect_posts(page, start_dt, end_dt)
            logger.info("found %d posts to process", len(shortcodes))

            # 각 게시물 상세 정보 수집
            for shortcode in shortcodes:
                await self._random_delay(5, 8)

                post_data = await self._parse_post_data(page, shortcode)
                if not post_data:
                    continue

                # 날짜 필터링
                if post_data.posted_at:
                    if post_data.posted_at < start_dt:
                        continue
                    if post_data.posted_at > end_dt:
                        continue

                # 키워드 필터링
                if search_keywords and not contains_any(post_data.content, search_keywords):
                    continue

                posts.append(
                    SocialPost(
                        brand_id=brand_id,
                        platform=self.platform,
                        external_post_id=post_data.post_id,
                        post_url=post_data.url,
                        content=post_data.content,
                        likes=post_data.likes,
                        comments=post_data.comments,
                        views=post_data.views,
                        posted_at=post_data.posted_at,
                        crawled_at=datetime.now(),
                        matched_keywords=[
                            k for k in search_keywords
                            if k and k.lower() in post_data.content.lower()
                        ],
                    )
                )

            return posts

        except Exception as e:
            logger.error("instagram crawl failed for @%s: %s", handle, e)
            return posts
        finally:
            elapsed_ms = int((time.perf_counter() - start_time) * 1000)
            logger.info(
                "instagram crawl done handle=%s found=%d elapsed_ms=%d",
                handle, len(posts), elapsed_ms
            )

    def crawl_search(
            self,
            brand_id: int,
            search_keywords: list[str],
            start_dt: datetime,
            end_dt: datetime,
    ) -> list[SocialPost]:
        """해시태그 검색 크롤링 (동기 래퍼)"""

        return None
        '''
        return asyncio.get_event_loop().run_until_complete(
            self._crawl_search_async(brand_id, search_keywords, start_dt, end_dt)
        )
        '''

    async def _crawl_search_async(
            self,
            brand_id: int,
            search_keywords: list[str],
            start_dt: datetime,
            end_dt: datetime,
    ) -> list[SocialPost]:
        """해시태그 검색 크롤링 (비동기)"""
        start_time = time.perf_counter()
        posts: list[SocialPost] = []

        try:
            context = await self._init_browser()
            page = await context.new_page()

            if not await self._check_login_status(page):
                if not await self._login(page):
                    return posts

            for keyword in search_keywords:
                tag = keyword.strip().lstrip("#")
                if not tag:
                    continue

                try:
                    # 해시태그 페이지로 이동
                    tag_url = f"{self.BASE_URL}/explore/tags/{tag}/"
                    await page.goto(tag_url, wait_until="networkidle")
                    await self._random_delay(2, 4)

                    # 게시물 수집
                    shortcodes = await self._scroll_and_collect_posts(
                        page, start_dt, end_dt, max_posts=20
                    )


                    for shortcode in shortcodes:
                        await self._random_delay(3, 6)

                        post_data = await self._parse_post_data(page, shortcode)
                        if not post_data:
                            continue

                        if post_data.posted_at:
                            if post_data.posted_at < start_dt:
                                continue
                            if post_data.posted_at > end_dt:
                                continue

                        posts.append(
                            SocialPost(
                                brand_id=brand_id,
                                platform=self.platform,
                                external_post_id=post_data.post_id,
                                post_url=post_data.url,
                                content=post_data.content,
                                likes=post_data.likes,
                                comments=post_data.comments,
                                views=post_data.views,
                                posted_at=post_data.posted_at,
                                crawled_at=datetime.now(),
                                matched_keywords=[keyword],
                            )
                        )

                except Exception as e:
                    logger.warning("instagram search failed for #%s: %s", tag, e)
                    continue

            return posts

        finally:
            elapsed_ms = int((time.perf_counter() - start_time) * 1000)
            logger.info(
                "instagram search done keywords=%d found=%d elapsed_ms=%d",
                len(search_keywords), len(posts), elapsed_ms
            )

    async def close(self) -> None:
        """브라우저 종료"""
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()

    def __del__(self) -> None:
        """소멸자에서 브라우저 정리"""
        try:
            if self._browser:
                asyncio.get_event_loop().run_until_complete(self.close())
        except Exception:
            pass
