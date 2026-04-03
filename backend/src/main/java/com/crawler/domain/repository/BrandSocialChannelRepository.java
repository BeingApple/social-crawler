package com.crawler.domain.repository;

import com.crawler.domain.entity.BrandSocialChannel;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface BrandSocialChannelRepository extends JpaRepository<BrandSocialChannel, Long> {

    List<BrandSocialChannel> findByBrandId(Long brandId);

    List<BrandSocialChannel> findByPlatformId(String platformId);

    Optional<BrandSocialChannel> findByBrandIdAndPlatformId(Long brandId, String platformId);
}