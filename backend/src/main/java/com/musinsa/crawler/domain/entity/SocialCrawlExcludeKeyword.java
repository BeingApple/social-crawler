package com.musinsa.crawler.domain.entity;

import jakarta.persistence.*;
import lombok.Getter;

import java.time.LocalDateTime;

@Entity
@Table(name = "social_crawl_exclude_keyword")
@Getter
public class SocialCrawlExcludeKeyword {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long keywordId;

    @Column(nullable = false, length = 20)
    private String keywordType;

    @Column(nullable = false, length = 50)
    private String platformId;

    private Long brandId;

    @Column(length = 500)
    private String filterKeyword;

    @Column(length = 500)
    private String junkKeyword;

    @Column(nullable = false, length = 20)
    private String matchType;

    @Column(length = 300)
    private String description;

    @Column(name = "is_active", nullable = false)
    private boolean active;

    @Column(length = 100)
    private String createdBy;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(nullable = false)
    private LocalDateTime updatedAt;
}