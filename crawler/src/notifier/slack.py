import requests


class SlackNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_summary(self, brand_name: str, platform: str, posts: list, ai_summary: dict) -> None:
        lines = [
            f"*[{brand_name}] {platform} 요약*",
            f"- 수집 건수: {len(posts)}",
        ]

        for item in ai_summary["platforms"]:
            lines.append(f"\n*{item['platform']}* ({item['count']}건)")
            for idx, post in enumerate(item["top_posts"], 1):
                lines.append(f"{idx}. {post['content']}")
                lines.append(f"   - 좋아요 {post['likes']} / 댓글 {post['comments']} / 조회수 {post['views']}")
                lines.append(f"   - {post['url']}")

        payload = {"text": "\n".join(lines)}
        resp = requests.post(self.webhook_url, json=payload, timeout=15)
        resp.raise_for_status()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(webhook_url={self.webhook_url!r})"
