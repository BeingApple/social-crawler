class CrawlError(Exception):
    pass


class RateLimitError(CrawlError):
    pass


class NotFoundError(CrawlError):
    pass


class AccessDeniedError(CrawlError):
    pass