package com.musinsa.crawler.domain.repository;

import com.musinsa.crawler.domain.entity.SocialPlatform;
import org.springframework.data.jpa.repository.JpaRepository;

public interface SocialPlatformRepository extends JpaRepository<SocialPlatform, String> {
}
