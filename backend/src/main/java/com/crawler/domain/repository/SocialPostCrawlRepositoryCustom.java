package com.crawler.domain.repository;

import com.crawler.domain.entity.SocialPostCrawl;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.time.LocalDateTime;

public interface SocialPostCrawlRepositoryCustom {

    Page<SocialPostCrawl> findWithFilters(
            String platformId,
            String brandName,
            String crawlCase,
            LocalDateTime postedFrom,
            LocalDateTime postedTo,
            Pageable pageable
    );
}
