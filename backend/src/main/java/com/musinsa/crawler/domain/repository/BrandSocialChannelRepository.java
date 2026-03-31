package com.musinsa.crawler.domain.repository;

import com.musinsa.crawler.domain.entity.BrandSocialChannel;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface BrandSocialChannelRepository extends JpaRepository<BrandSocialChannel, Long> {

    List<BrandSocialChannel> findByBrandId(Long brandId);

    List<BrandSocialChannel> findByPlatformId(String platformId);
}