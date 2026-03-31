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
    private String assigneeName;
    private String accountId;
    private String accountType;
    private boolean active;

    public static AssigneeResponse from(BrandAssignee a) {
        return AssigneeResponse.builder()
                .assigneeId(a.getAssigneeId())
                .brandId(a.getBrand() != null ? a.getBrand().getBrandId() : null)
                .brandName(a.getBrand() != null ? a.getBrand().getBrandName() : null)
                .platformId(a.getPlatformId())
                .assigneeName(a.getAssigneeName())
                .accountId(a.getAccountId())
                .accountType(a.getAccountType())
                .active(a.isActive())
                .build();
    }
}