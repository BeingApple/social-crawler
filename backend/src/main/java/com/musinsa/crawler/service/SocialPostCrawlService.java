package com.musinsa.crawler.service;

import com.musinsa.crawler.api.dto.SocialPostCrawlResponse;
import com.musinsa.crawler.domain.repository.SocialPostCrawlRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class SocialPostCrawlService {

    private final SocialPostCrawlRepository postRepository;

    public Page<SocialPostCrawlResponse> findPosts(
            String platformId,
            String brandName,
            String crawlCase,
            LocalDate postedFrom,
            LocalDate postedTo,
            Pageable pageable
    ) {
        LocalDateTime fromDt = postedFrom != null ? postedFrom.atStartOfDay()            : null;
        LocalDateTime toDt   = postedTo   != null ? postedTo.plusDays(1).atStartOfDay()  : null;

        return postRepository
                .findWithFilters(platformId, brandName, crawlCase, fromDt, toDt, pageable)
                .map(SocialPostCrawlResponse::from);
    }

    public Optional<SocialPostCrawlResponse> findPost(Long spcId) {
        return postRepository.findById(spcId)
                .map(SocialPostCrawlResponse::from);
    }
}
