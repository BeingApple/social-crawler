package com.crawler.api.dto;

import lombok.Builder;
import lombok.Getter;

/** 복호화된 원문 자격증명 응답 — GET /api/crawl-accounts/{id}/decrypt 전용 */
@Getter
@Builder
public class SocialCrawlAccountCredentialResponse {

    private Long accountId;
    private String platformId;
    private String loginId;
    private String loginPw;
}
