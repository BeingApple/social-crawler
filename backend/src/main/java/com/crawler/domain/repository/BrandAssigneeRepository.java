package com.crawler.domain.repository;

import com.crawler.domain.entity.BrandAssignee;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface BrandAssigneeRepository extends JpaRepository<BrandAssignee, Long> {

    List<BrandAssignee> findByBrand_BrandId(Long brandId);

    List<BrandAssignee> findByPlatformIdAndActive(String platformId, boolean active);
}
