package com.musinsa.crawler.api.controller;

import com.musinsa.crawler.api.dto.AssigneeResponse;
import com.musinsa.crawler.domain.entity.BrandAssignee;
import com.musinsa.crawler.domain.repository.BrandAssigneeRepository;
import com.musinsa.crawler.domain.repository.BrandSocialChannelRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/assignees")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")   // 개발용. 운영 시 도메인 명시
public class AssigneeController {

    private final BrandAssigneeRepository assigneeRepository;
    private final BrandSocialChannelRepository channelRepository;

    /** 담당자(계정) 전체 목록 — 프론트에서 클라이언트 사이드 필터링 */
    @GetMapping
    public ResponseEntity<List<AssigneeResponse>> list() {
        List<AssigneeResponse> result = assigneeRepository.findAll()
                .stream()
                .map(this::toResponse)
                .toList();
        return ResponseEntity.ok(result);
    }

    private AssigneeResponse toResponse(BrandAssignee a) {
        Long brandId = a.getBrand() != null ? a.getBrand().getBrandId() : null;
        String region = brandId != null
                ? channelRepository.findByBrandIdAndPlatformId(brandId, a.getPlatformId())
                        .map(ch -> ch.getRegion())
                        .orElse(null)
                : null;
        return AssigneeResponse.from(a, region);
    }
}