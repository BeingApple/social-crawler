package com.musinsa.crawler.domain.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "social_crawl_account")
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SocialCrawlAccount {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long accountId;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, length = 50)
    private String platformId;

    /** 암호화된 로그인 ID (AES-256-GCM + Base64) */
    @Column(nullable = false, length = 200)
    private String loginId;

    /** 암호화된 로그인 PW (AES-256-GCM + Base64) */
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

    @PrePersist
    protected void onCreate() {
        createdAt = updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }

    public void update(String name, String platformId, String loginId, String loginPw,
                       String issue, String status) {
        this.name = name;
        this.platformId = platformId;
        this.loginId = loginId;
        this.loginPw = loginPw;
        this.issue = issue;
        this.status = status;
    }
}