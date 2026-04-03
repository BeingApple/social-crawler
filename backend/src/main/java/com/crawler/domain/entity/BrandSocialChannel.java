package com.crawler.domain.entity;

import jakarta.persistence.*;
import lombok.Getter;

import java.time.LocalDateTime;

@Entity
@Table(name = "brand_social_channel")
@Getter
public class BrandSocialChannel {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long channelId;

    @Column(nullable = false)
    private Long brandId;

    @Column(nullable = false, length = 50)
    private String platformId;

    @Column(nullable = false, length = 10)
    private String region;

    @Column(length = 200)
    private String channelUrl;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(nullable = false)
    private LocalDateTime updatedAt;
}