package com.crawler.service;

import com.crawler.api.dto.AssigneeResponse;
import com.crawler.domain.entity.BrandAssignee;
import com.crawler.domain.repository.BrandAssigneeRepository;
import com.crawler.domain.repository.BrandSocialChannelRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class AssigneeService {

    private final BrandAssigneeRepository assigneeRepository;
    private final BrandSocialChannelRepository channelRepository;

    public List<AssigneeResponse> findAllAssignees() {
        return assigneeRepository.findAll()
                .stream()
                .map(this::toResponse)
                .toList();
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
