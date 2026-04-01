package com.musinsa.crawler.api.dto;

import com.musinsa.crawler.domain.entity.SocialCrawlAccount;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;

@Getter
@Builder
public class SocialCrawlAccountResponse {

    private Long accountId;
    private String name;
    private String platformId;
    private String loginId;   // 복호화된 loginId
    private String status;
    private String issue;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public static SocialCrawlAccountResponse from(SocialCrawlAccount entity, String decryptedLoginId) {
        return SocialCrawlAccountResponse.builder()
                .accountId(entity.getAccountId())
                .name(entity.getName())
                .platformId(entity.getPlatformId())
                .loginId(decryptedLoginId)
                .status(entity.getStatus())
                .issue(entity.getIssue())
                .createdAt(entity.getCreatedAt())
                .updatedAt(entity.getUpdatedAt())
                .build();
    }
}
