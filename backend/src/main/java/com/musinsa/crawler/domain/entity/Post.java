package com.musinsa.crawler.domain.entity;

import jakarta.persistence.*;
import lombok.Getter;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "post")
@Getter
public class Post {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long postId;

    @Column(nullable = false)
    private Long brandId;

    @Column(nullable = false, length = 30)
    private String platform;

    @Column(nullable = false, length = 200)
    private String externalPostId;

    @Lob
    private String content;

    @JdbcTypeCode(SqlTypes.JSON)
    private List<String> mediaUrls;

    @JdbcTypeCode(SqlTypes.JSON)
    private List<String> hashtags;

    private int likes;
    private int comments;
    private int shares;
    private long views;

    private LocalDateTime postedAt;

    @Column(nullable = false, updatable = false)
    private LocalDateTime crawledAt = LocalDateTime.now();
}
