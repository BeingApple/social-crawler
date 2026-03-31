package com.musinsa.crawler.domain.repository;

import com.musinsa.crawler.domain.entity.SocialPostCrawl;
import org.springframework.data.jpa.repository.JpaRepository;

public interface SocialPostCrawlRepository extends JpaRepository<SocialPostCrawl, Long>, SocialPostCrawlRepositoryCustom {
}
