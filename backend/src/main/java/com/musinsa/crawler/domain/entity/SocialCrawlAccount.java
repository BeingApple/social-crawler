package com.musinsa.crawler.domain.entity;

import jakarta.persistence.*;
import lombok.Getter;

import java.time.LocalDateTime;

@Entity
@Table(name = "social_crawl_account")
@Getter
public class SocialCrawlAccount {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long accountId;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, length = 50)
    private String platformId;

    @Column(nullable = false, length = 200)
    private String loginId;

    @Column(nullable = false, length = 500)
    private String loginPw;

    @Lob
    private String issue;

    @Column(nullable = false, length = 20)
    private String status;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(nullable = false)
    private LocalDateTime updatedAt;
}