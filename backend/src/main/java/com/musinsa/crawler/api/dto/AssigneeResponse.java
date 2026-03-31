package com.musinsa.crawler.api.dto;

import com.musinsa.crawler.domain.entity.BrandAssignee;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class AssigneeResponse {

    private Long assigneeId;
    private Long brandId;
    private String brandName;
    private String platformId;
    private String region;
    private String assigneeName;
    private String accountId;
    private boolean active;

    public static AssigneeResponse from(BrandAssignee a, String region) {
        return AssigneeResponse.builder()
                .assigneeId(a.getAssigneeId())
                .brandId(a.getBrand() != null ? a.getBrand().getBrandId() : null)
                .brandName(a.getBrand() != null ? a.getBrand().getBrandName() : null)
                .platformId(a.getPlatformId())
                .region(region)
                .assigneeName(a.getAssigneeName())
                .accountId(a.getAccountId())
                .active(a.isActive())
                .build();
    }
}