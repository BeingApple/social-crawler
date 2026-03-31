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
            grouped[post.platform_id].append(post)

        platform_summaries = []
        for platform_id, items in grouped.items():
            top_items = sorted(
                items,
                key=lambda p: ((p.like_count or 0) + (p.comment_count or 0) + (p.view_count or 0)),
                reverse=True,
            )[:5]
            platform_summaries.append({
                "platform": platform_id,
                "count": len(items),
                "top_posts": [
                    {
                        "url": p.post_url,
                        "content": (p.text_content or "")[:120],
                        "likes": p.like_count,
                        "comments": p.comment_count,
                        "views": p.view_count,
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
        return f"{self.__class__.__name__}()"