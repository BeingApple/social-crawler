from collections import defaultdict

from src.common.types import SocialPost


class ContentFilter:
    def should_skip(self, content: str, junk_keywords: list[str]) -> bool:
        text = (content or "").lower()
        return any(k.lower() in text for k in junk_keywords if k)


class SummaryService:
    def summarize(self, brand_name: str, posts: list[SocialPost]) -> dict:
        grouped = defaultdict(list)
        for post in posts:
            grouped[post.platform].append(post)

        platform_summaries = []
        for platform, items in grouped.items():
            top_items = sorted(items, key=lambda p: (p.likes + p.comments + p.views), reverse=True)[:5]
            platform_summaries.append({
                "platform": platform,
                "count": len(items),
                "top_posts": [
                    {
                        "url": p.post_url,
                        "content": p.content[:120],
                        "likes": p.likes,
                        "comments": p.comments,
                        "views": p.views,
                    }
                    for p in top_items
                ],
            })

        return {
            "brand_name": brand_name,
            "total_count": len(posts),
            "platforms": platform_summaries,
        }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(brand_name={self.brand_name!r})"