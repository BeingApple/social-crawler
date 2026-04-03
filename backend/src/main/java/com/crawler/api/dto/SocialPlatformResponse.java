package com.crawler.api.dto;

import com.crawler.domain.entity.SocialPlatform;
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
