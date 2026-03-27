import time
import requests


class HttpClient:
    def __init__(self, timeout: int = 15):
        self.session = requests.Session()
        self.timeout = timeout

        self.session.headers.update({
            "User-Agent": "brand-social-crawler/1.0",
            "Accept": "application/json,text/html,application/xhtml+xml",
            "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
        })

    def get(self, url: str, params: dict | None = None, retries: int = 3) -> requests.Response:
        last_error = None

        for attempt in range(retries):
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)

                if response.status_code == 429:
                    sleep_sec = 2 ** attempt
                    time.sleep(sleep_sec)
                    continue

                return response
            except requests.RequestException as e:
                last_error = e
                time.sleep(2 ** attempt)

        raise last_error