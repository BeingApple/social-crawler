package com.musinsa.crawler.domain.repository;

import com.musinsa.crawler.domain.entity.Post;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PostRepository extends JpaRepository<Post, Long> {

    Page<Post> findByPlatform(String platform, Pageable pageable);

    Page<Post> findByBrandId(Long brandId, Pageable pageable);
}
