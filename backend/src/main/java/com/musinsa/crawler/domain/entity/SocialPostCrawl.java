package com.musinsa.crawler.domain.entity;

import jakarta.persistence.*;
import lombok.Getter;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.time.LocalDateTime;
import java.util.Map;

@Entity
@Table(name = "social_post_crawl")
@Getter
public class SocialPostCrawl {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long spcId;

    // 수집 메타
    @Column(nullable = false, length = 50)
    private String platformId;

    @Column(nullable = false, length = 10)
    private String crawlCase;

    @Column(nullable = false, length = 100)
    private String brandName;

    @Column(nullable = false, length = 200)
    private String accountId;

    @Column(nullable = false, length = 10)
    private String accountType;

    // 게시물 정보
    @Column(nullable = false, length = 200)
    private String postId;

    @Column(nullable = false, length = 500)
    private String postUrl;

    @Column(length = 30)
    private String postType;

    @Column(nullable = false)
    private LocalDateTime postedAt;

    @Column(length = 255)
    private String postTitle;

    @Lob
    private String textContent;

    @Lob
    private String personTags;

    @Lob
    private String hashtags;

    @Column(length = 500)
    private String mediaUrl;

    // 통계
    private Long viewCount;
    private Long likeCount;
    private Long commentCount;
    private Long shareCount;

    // CASE2 전용
    @Lob
    private String matchedKeywords;

    @Column(length = 200)
    private String authorName;

    private Long authorFollowers;

    // 플래그
    @Column(name = "is_duplicate", nullable = false)
    private boolean duplicate;

    @Column(name = "is_junk", nullable = false)
    private boolean junk;

    // 원본 데이터
    @JdbcTypeCode(SqlTypes.JSON)
    private Map<String, Object> rawData;

    // 타임스탬프
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(nullable = false)
    private LocalDateTime updatedAt;
}