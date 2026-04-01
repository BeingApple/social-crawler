package com.musinsa.crawler.api.dto;

import com.musinsa.crawler.domain.entity.SocialPlatform;
import lombok.Getter;

@Getter
public class SocialPlatformResponse {

    private final String platformId;
    private final String platformName;

    private SocialPlatformResponse(SocialPlatform p) {
        this.platformId   = p.getPlatformId();
        this.platformName = p.getPlatformName();
    }

    public static SocialPlatformResponse from(SocialPlatform p) {
        return new SocialPlatformResponse(p);
    }
}
