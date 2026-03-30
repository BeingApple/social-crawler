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
from zoneinfo import ZoneInfo
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
            // webdriver 플래그 제거
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

            // 모바일(iPhone)은 plugins 없음
            Object.defineProperty(navigator, 'plugins', { get: () => [] });

            // 언어 설정 (ko-KR 우선)
            Object.defineProperty(navigator, 'languages', { get: () => ['ko-KR', 'ko', 'en-US', 'en'] });

            // 하드웨어 스펙 (iPhone 14 Pro Max 수준)
            Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 6 });
            Object.defineProperty(navigator, 'platform', { get: () => 'iPhone' });

            // window.chrome 객체 (모바일 Chrome에도 존재)
            if (!window.chrome) {
                window.chrome = {
                    runtime: {},
                    loadTimes: () => {},
                    csi: () => {},
                };
            }

            // Notification 권한 쿼리 우회 (headless 기본값 노출 방지)
            if (navigator.permissions && navigator.permissions.query) {
                const _origQuery = navigator.permissions.query.bind(navigator.permissions);
                navigator.permissions.query = (params) => {
                    if (params && params.name === 'notifications') {
                        return Promise.resolve({ state: 'denied', onchange: null });
                    }
                    return _origQuery(params);
                };
            }
        """)

        return self._context

    async def _login(self, page: Page) -> bool:
        """Instagram 로그인 수행"""
        if not self._username or not self._password:
            logger.warning("instagram credentials not set")
            return False

        try:
            await page.goto(f"{self.BASE_URL}/accounts/login/", wait_until="load")
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
            await page.goto(self.BASE_URL, wait_until="load", timeout=30000)
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

    @staticmethod
    def _node_to_post_data(node: dict) -> InstagramPageData | None:
        """GraphQL 응답 노드에서 게시물 데이터 추출"""
        try:
            shortcode = node.get("code", "")
            if not shortcode:
                return None

            caption = node.get("caption") or {}
            content = caption.get("text", "") if isinstance(caption, dict) else ""

            taken_at = node.get("taken_at")
            posted_at = datetime.fromtimestamp(taken_at, tz=ZoneInfo("Asia/Seoul")) if taken_at else None

            views = node.get("view_count") or node.get("play_count") or 0

            return InstagramPageData(
                post_id=shortcode,
                url=f"https://www.instagram.com/p/{shortcode}/",
                content=content,
                likes=node.get("like_count", 0),
                comments=node.get("comment_count", 0),
                views=views,
                posted_at=posted_at,
            )
        except Exception as e:
            logger.warning("failed to parse graphql node: %s", e)
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

    async def _scroll_and_intercept_graphql(
            self,
            page: Page,
            profile_url: str,
            max_posts: int = 50,
            max_scroll_attempts: int = 10,
    ) -> tuple[list[dict], int]:
        """프로필 페이지 이동 전에 리스너를 등록하고, 첫 로드 + 스크롤 중 GraphQL 응답 수집"""
        nodes: list[dict] = []
        seen_ids: set[str] = set()  # pk와 code 모두 추적
        follower_count: int = 0
        last_height = 0
        scroll_attempts = 0

        async def on_response(response) -> None:
            nonlocal follower_count
            if "graphql/query" not in response.url or response.status != 200:
                return
            try:
                body = await response.json()
                # 팔로워 수 (처음 한 번만 캡처)
                if not follower_count:
                    follower_count = (
                        body.get("data", {})
                        .get("user", {})
                        .get("follower_count", 0)
                    )
                timeline = (
                    body.get("data", {})
                    .get("xdt_api__v1__feed__user_timeline_graphql_connection", {})
                )
                if not timeline:
                    return
                for edge in timeline.get("edges", []):
                    node = edge.get("node", {})
                    pk = str(node.get("pk", ""))
                    code = node.get("code", "")
                    # pk 또는 code 중 하나라도 이미 수집한 경우 스킵
                    if (pk and pk in seen_ids) or (code and code in seen_ids):
                        continue
                    if pk:
                        seen_ids.add(pk)
                    if code:
                        seen_ids.add(code)
                    nodes.append(node)
            except Exception:
                pass

        # goto 전에 리스너 등록 → 첫 페이지 로드의 GraphQL 응답도 캡처
        page.on("response", on_response)

        try:
            await page.goto(profile_url, wait_until="load", timeout=30000)
            await self._random_delay(10, 15)

            while len(nodes) < max_posts and scroll_attempts < max_scroll_attempts:
                # 페이지 높이 변화 감지 (종료 조건 판단)
                current_height = await page.evaluate("document.body.scrollHeight")
                if current_height == last_height:
                    scroll_attempts += 1
                else:
                    scroll_attempts = 0
                last_height = current_height

                # 뷰포트의 60~100% 범위를 4~8 단계로 나눠 스크롤 (사람 패턴 모사)
                viewport_height = await page.evaluate("window.innerHeight")
                scroll_target = int(viewport_height * random.uniform(0.6, 1.0))
                steps = random.randint(4, 8)
                step_size = scroll_target // steps
                for _ in range(steps):
                    jitter = random.randint(-10, 10)
                    await page.evaluate(f"window.scrollBy(0, {step_size + jitter})")
                    await asyncio.sleep(random.uniform(0.05, 0.18))

                await self._random_delay(1.5, 3)
        finally:
            page.remove_listener("response", on_response)

        return nodes[:max_posts], follower_count

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

            logger.info("instagram crawl started for @%s", handle)

            # 리스너 등록 → 첫 로드 + 스크롤 중 GraphQL 응답을 모두 캡처
            profile_url = f"{self.BASE_URL}/{handle}/"
            nodes, follower_count = await self._scroll_and_intercept_graphql(page, profile_url, max_posts=50)
            logger.info("instagram @%s follower_count=%d", handle, follower_count)

            # 프로필 존재 확인 (goto 이후 현재 URL/콘텐츠 기준)
            if "페이지를 찾을 수 없습니다" in await page.content():
                logger.warning("instagram profile not found: %s", handle)
                return posts
            logger.info("found %d posts via graphql", len(nodes))

            for node in nodes:
                post_data = self._node_to_post_data(node)
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

            logger.info(posts)
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
                    # 리스너 등록 → 첫 로드 + 스크롤 중 GraphQL 응답을 모두 캡처
                    tag_url = f"{self.BASE_URL}/explore/tags/{tag}/"
                    nodes, _ = await self._scroll_and_intercept_graphql(page, tag_url, max_posts=20)

                    for node in nodes:
                        post_data = self._node_to_post_data(node)
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
