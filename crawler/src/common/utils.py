from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import random

# User-Agent 목록 (로테이션용)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
]

def yesterday_range() -> tuple[datetime, datetime]:
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    yesterday = now - timedelta(days=1)
    #start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    testDay = now - timedelta(days=10)
    start = testDay.replace(hour=0, minute=0, second=0, microsecond=0)

    end = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
    return start, end


def normalize_text(value: str | None) -> str:
    return (value or "").strip().lower()


def contains_any(text: str, keywords: list[str]) -> bool:
    normalized = normalize_text(text)
    return any(normalize_text(k) in normalized for k in keywords if k)

# User-Agent 목록 (로테이션용)
def random_user_agent() -> str:
    """랜덤 User-Agent 반환"""
    return random.choice(USER_AGENTS)


def rotate_session(self, proxy: dict[str, str] | None = None) -> None:
    """세션 로테이션 (프록시/User-Agent 변경)"""
    new_ua = random_user_agent()
    self.loader.context.user_agent = new_ua

    if proxy:
        self.loader.context.proxy = proxy
