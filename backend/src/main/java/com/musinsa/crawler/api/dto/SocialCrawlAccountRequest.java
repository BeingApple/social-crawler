package com.musinsa.crawler.api.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Getter;

@Getter
public class SocialCrawlAccountRequest {

    @NotBlank
    @Size(max = 100)
    private String name;

    @NotBlank
    @Size(max = 50)
    private String platformId;

    @NotBlank
    @Size(max = 200)
    private String loginId;

    @NotBlank
    @Size(max = 500)
    private String loginPw;

    private String issue;

    @NotBlank
    @Pattern(regexp = "ACTIVE|BLOCKED|EXPIRED|PAUSED")
    private String status;
}
