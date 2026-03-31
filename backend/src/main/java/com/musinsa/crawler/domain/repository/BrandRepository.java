package com.musinsa.crawler.domain.repository;

import com.musinsa.crawler.domain.entity.Brand;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface BrandRepository extends JpaRepository<Brand, Long> {

    Optional<Brand> findByBrandName(String brandName);
}